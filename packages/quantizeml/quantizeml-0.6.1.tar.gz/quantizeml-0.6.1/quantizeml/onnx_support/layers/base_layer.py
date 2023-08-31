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
__all__ = ["OnnxLayer"]

from onnx.helper import make_function, make_node, make_opsetid
from onnx.defs import onnx_opset_version

from .register import register_new_subgraph, infer_function_parameters
from .graph_tools import to_field

DOMAIN = "com.brainchip"
VERSION = 1


def get_brainchip_opsetid():
    """Get the opset id given a target akida version.

    Returns:
        OperatorSetIdProto: the opset id
    """
    return make_opsetid(DOMAIN, VERSION)


class OnnxLayer:
    """Abstract class that represents an onnx subgraph in brainchip domain.

    Child must define the attributes on __init__ and return the node list (subgraph) on
    build_subgraph(). If these requirements are met, make_node() could be used to
    define/register the custom node.

    Args:
        op_type (str): the operation type name.
        opset_imports (list of OperatorSetIdProto, optional): the custom opset. Defaults to None.
        kwargs (dict, optional): the custom attributes. Each attribute type will be
            infered by ``onnx.helper.make_attribute()``. Defaults to {}.
    """

    def __init__(self, op_type, opset_imports=None, **kwargs):
        self.op_type = op_type
        self._opset_imports = opset_imports or [make_opsetid("", onnx_opset_version())]

        # Load attributes
        # Note: this field is called 'attribute' to align it to the same ONNX standard
        self.attribute = self._load_attributes(**kwargs)

    @property
    def opset_imports(self):
        return self._opset_imports + [get_brainchip_opsetid()]

    def _load_attributes(self, **kwargs):
        attrs = []
        for key, value in kwargs.items():
            # Convert each value in an AttributeProto
            value = to_field(key, value)
            attrs.append(value)
        return attrs

    @staticmethod
    def build_subgraph(op_type):
        """Define the subgraph

        Args:
            op_type (str): operation type to build

        Returns:
            list of NodeProto: the operation sequence.
        """
        raise NotImplementedError("Child must implement this function")

    def make_node(self, inputs, outputs, name=None):
        """Return the NodeProto, setting the attributes.

        Args:
            inputs (list of str): list of input names.
            outputs (list of str): list of output names.
            name (str, optional): unique identifier for NodeProto. Defaults to None.

        Returns:
            NodeProto: the corresponding node.
        """
        # Build the subgraph (implemented in derived classes) and register subgraph
        # to make it available, unless previously registered already
        nodes = self.build_subgraph(self.op_type)
        inputs_fn, outputs_fn, attributes_fn = infer_function_parameters(nodes)
        func = make_function(domain=DOMAIN,
                             fname=self.op_type,
                             inputs=inputs_fn,
                             outputs=outputs_fn,
                             nodes=nodes,
                             opset_imports=self._opset_imports,
                             attributes=attributes_fn)
        register_new_subgraph(func)

        # Return the node with corresponding attributes
        node = make_node(self.op_type, inputs=inputs, outputs=outputs, name=name, domain=DOMAIN)
        consume_attrs = [attr for attr in self.attribute if attr.name in func.attribute]
        node.attribute.extend(consume_attrs)
        return node
