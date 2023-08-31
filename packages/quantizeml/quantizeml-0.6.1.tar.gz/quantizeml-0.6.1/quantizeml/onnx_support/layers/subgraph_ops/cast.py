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
__all__ = ["cast_tensors_to"]

from onnx import TensorProto as TP
from onnx.helper import make_node


def cast_tensors_to(in_names, out_names, dtype=TP.FLOAT):
    """Cast tensors to a given type.

    Args:
        in_names (list): list of input tensor names.
        out_names (list): list of output tensor names
        dtype (DataType, optional): the type to cast. Defaults to TensorProto.FLOAT

    Returns:
        NodeProto list: list of cast nodes.
    """
    # Cast tensors to float
    nodes = []
    for in_name, out_name in zip(in_names, out_names):
        nodes.append(make_node("Cast", [in_name], [out_name], to=dtype))
    return nodes
