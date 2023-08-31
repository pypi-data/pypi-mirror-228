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
__all__ = ["QuantizedDepthwise2D"]

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops
from .subgraph_ops.serialize import get_serialized_op_name


class QuantizedDepthwise2D(OnnxLayer):
    """Intermediate representation of Conv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        groups (int, optional): the number of groups input channels and
            output channels are divided into. Defaults to 1.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        max_value (bool, optional): whether there is going to be a max value to apply
            to the ReLU activation. Ignored when activation is False. Defaults to False.
        use_bias (bool, optional): whether to apply bias in convolution. Defaults to False.
    """

    def __init__(self,
                 strides=[1, 1],
                 groups=1,
                 activation=False,
                 max_value=False,
                 use_bias=False):
        # Serialize attributes in operation name
        base_name = get_serialized_op_name("QuantizedDepthwise2D",
                                           use_bias=use_bias,
                                           activation=activation,
                                           max_value=max_value)

        super().__init__(base_name, groups=groups, strides=strides)

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        nodes = cast_tensors_to(["X", "W"], ["Xq", "Wi"])
        bias_name = ""
        if "Biased" in op_type:
            bias_name = "Bi"
            nodes += cast_tensors_to(["bias"], [bias_name])

        # Pad + convolution
        nodes += get_padding_ops("Xq", "Xi")
        nodes.append(make_node("Conv", inputs=["Xi", "Wi", bias_name], outputs=["Yi"]))
        # Constrain attribute that we allow
        nodes[-1].attribute.extend([AP(name="strides", ref_attr_name="strides", type=AP.INTS),
                                   AP(name="group", ref_attr_name="groups", type=AP.INT)])

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Scale out (with saturation) in float domain
        nodes += cast_tensors_to(["Scale", "Shift"], ["Scf", "Shf"])
        nodes += get_scale_out_ops("Yi", "Yscaled", "Scf", "Shf")
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
