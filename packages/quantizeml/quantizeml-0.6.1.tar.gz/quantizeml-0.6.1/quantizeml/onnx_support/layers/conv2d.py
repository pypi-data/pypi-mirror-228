#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ["QuantizedConv2D"]

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_pool_ops, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops
from .subgraph_ops.serialize import get_serialized_op_name


class QuantizedConv2D(OnnxLayer):
    """Intermediate representation of QLinearConv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        pool_type (str, optional): the pool type, one of {"none", "max"}. Defaults to "none".
        pool_size (list of int, optional): the kernel pool shape.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_stride (list of int, optional): the kernel strides.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_pads (list of int, optional): the size of each padding dimension.
            Ignore it when pool_type != "max". Defaults to [0, 0, 0, 0].
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        max_value (bool, optional): whether there is going to be a max value to apply
            to the ReLU activation. Ignored when activation is False. Defaults to False.
        use_bias (bool, optional): whether to apply bias in convolution. Defaults to False.
    """

    def __init__(self,
                 strides=[1, 1],
                 pool_type="none",
                 pool_size=(2, 2),
                 pool_strides=(2, 2),
                 pool_pads=[0, 0, 0, 0],
                 activation=False,
                 max_value=False,
                 use_bias=False):
        assert pool_type in ["none", "max", "gap"]

        # Serialize attributes in operation name
        base_name = get_serialized_op_name("QuantizedConv2D",
                                           use_bias=use_bias,
                                           pool_type=pool_type,
                                           activation=activation,
                                           max_value=max_value)

        super().__init__(base_name,
                         strides=strides,
                         pool_size=pool_size,
                         pool_strides=pool_strides,
                         pool_pads=pool_pads)

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        nodes = cast_tensors_to(["X", "x_pad_value", "W"], ["Xq", "XPadValue", "Wi"])
        bias_name = ""
        if "Biased" in op_type:
            bias_name = "Bi"
            nodes += cast_tensors_to(["bias"], [bias_name])

        # Pad + convolution
        nodes += get_padding_ops("Xq", "Xi", "XPadValue")
        nodes.append(make_node("Conv", inputs=["Xi", "Wi", bias_name], outputs=["Yi"]))
        nodes[-1].attribute.append(AP(name="strides", ref_attr_name="strides", type=AP.INTS))

        # Maxpool (optional)
        if "MaxPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="MaxPool")

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # AvgPool (optional)
        if "GlobalAvgPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="GlobalAvgPool")

        # Scale out (with saturation) in float domain
        nodes += cast_tensors_to(["Scale", "Shift"], ["Scf", "Shf"])
        nodes += get_scale_out_ops("Yi", "Yscaled", "Scf", "Shf")
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
