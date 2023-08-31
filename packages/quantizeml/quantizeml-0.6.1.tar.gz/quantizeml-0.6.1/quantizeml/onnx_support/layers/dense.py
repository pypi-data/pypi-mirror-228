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
__all__ = ["QuantizedDense1D"]

from onnx import TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.serialize import get_serialized_op_name


class QuantizedDense1D(OnnxLayer):
    """Intermediate representation of Flatten() + QGemm() + ReLU() as an exportable node.

    Args:
        flatten (bool, optional): whether to flatten the inputs. Defaults to False.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        max_value (bool, optional): whether there is going to be a max value to apply
            to the ReLU activation. Ignored when activation is False. Defaults to False.
        use_bias (bool, optional): whether to apply bias in matmul. Defaults to False.
        scale (bool, optional): whether scale the output. Defautls to True.
    """

    def __init__(self,
                 flatten=False,
                 activation=False,
                 max_value=False,
                 use_bias=False,
                 scale=True):
        # Serialize attributes in operation name
        base_name = get_serialized_op_name("QuantizedDense1D",
                                           use_bias=use_bias,
                                           flatten=flatten,
                                           activation=activation,
                                           max_value=max_value,
                                           scale=scale)
        super().__init__(base_name)

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        nodes = cast_tensors_to(["X", "W"], ["Xi", "Wi"])
        bias_name = ""
        if "Biased" in op_type:
            bias_name = "Bi"
            nodes += cast_tensors_to(["bias"], [bias_name])

        # Flatten (optional)
        x_name = "Xi"
        if "Flatten" in op_type:
            x_name = "Xflat"
            nodes.append(make_node("Flatten", inputs=["Xi"], outputs=[x_name]))

        # Gemm
        nodes.append(make_node("Gemm", inputs=[x_name, "Wi", bias_name], outputs=["Yi"], transB=1))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Apply final scale (with saturation) (optional)
        if "Scaled" in op_type:
            nodes += cast_tensors_to(["Scale", "Shift"], ["Scf", "Shf"])
            nodes += get_scale_out_ops("Yi", "Yscaled", "Scf", "Shf", saturate=True)
            nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Yi"], ["Y"], to=TP.INT32))
        return nodes
