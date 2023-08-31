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
__all__ = ["find_by_name", "get_tensor_shape", "get_tensor_dtype", "array_to_tp", "to_field",
           "set_by_name", "replace_field", "infer_shapes", "infer_partial_io",
           "get_next_neighbor_nodes"]

import numpy as np
import tempfile
from pathlib import Path
from copy import deepcopy

from onnx import numpy_helper as np_onnx
import onnx
from onnx.helper import make_attribute
from onnxruntime.quantization.quant_utils import load_model


def infer_shapes(model):
    """Helper function to infer all shapes in a model.

    Args:
        model (ModelProto): the model to infer the shapes.

    Returns:
        ModelProto: the model with all shapes inferred.
    """
    model = deepcopy(model)
    with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
        # To perfom ONNXRuntime optimization, we would like to use
        # onnxruntime.quantization.optimize_model, to split any model in primitive nodes.
        # onnx.shape_inference.infer_shape works with this kind of models.
        model_path = Path(f"{quant_tmp_dir}/model.onnx")
        onnx.save_model(model, model_path.as_posix())
        opt_model = load_model(model_path, need_optimize=True)

    # Clone all value info that match with current model
    model.graph.ClearField("value_info")
    in_names = sum([list(x.input) for x in model.graph.node], [])
    model.graph.value_info.extend([vi for vi in opt_model.graph.value_info if vi.name in in_names])

    return model


def find_by_name(item_name, item_list):
    """Helper function to find item by name in a list.

    Args:
        item_name (str): name of the item.
        item_list (list of Object): list of items.

    Returns:
        Object: item if found, None otherwise.
    """
    items = [item for item in item_list if item.name == item_name]
    assert len(items) < 2, "Duplicate elements found !"
    return items[0] if len(items) > 0 else None


def set_by_name(item_name, item_list, new_item):
    """Helper function to set an item into the list in the position
    which name matches.

    Args:
        item_name (str): name of the item.
        item_list (list of Object): list of items.
        new_item (Object): new item. the type must match with other items.
    """
    old_item = [(idx, item) for idx, item in enumerate(item_list) if item.name == item_name]
    if len(old_item) != 1:
        raise ValueError(f"Impossible to replace {item_name}: duplicated or missing in item list!")
    idx, old_item = old_item[0]
    assert type(old_item) == type(new_item), f"Incompatible type. Expected {type(old_item)}."
    # Update new element in list, avoiding direct assignment
    item_list.pop(idx)
    item_list.insert(idx, new_item)


def get_tensor_value_info(tensor_name, graph):
    """Helper to read the value info of one tensor.

    Args:
        tensor_name (str): the tensor to read the value info.
        graph (GraphProto): the graph containing the tensor.

    Returns:
        ValueInfoProto: the tensor value info.
    """
    # When input tensor is the graph input/output, its information is directly saved
    # in graph.input/graph.output attributes. Therefore, we allowed to search the
    # tensor information in the next fields:
    def _value_info_proto_to_dict(vip):
        return {el.name: el for el in vip}

    # Creating a dictionary allows to avoid the duplicate info problem (that happens on the output)
    tensors_dict = _value_info_proto_to_dict(graph.value_info)
    tensors_dict.update(_value_info_proto_to_dict(graph.input))
    tensors_dict.update(_value_info_proto_to_dict(graph.output))
    node_info = find_by_name(tensor_name, tensors_dict.values())
    if not node_info:
        raise RuntimeError(f"Element with name {tensor_name} not found in graph value info. "
                           "Before calling this function, run infer_shapes().")
    return node_info


def get_tensor_shape(tensor_name, graph):
    """Helper to read the shape of one tensor.

    Args:
        tensor_name (str): the tensor to read the shape.
        graph (GraphProto): the graph containing the tensor.

    Returns:
        tuple of ints: the tensor shape
    """
    node_info = get_tensor_value_info(tensor_name, graph)
    tensor_shape = node_info.type.tensor_type.shape.dim
    if len(tensor_shape) == 0:
        raise RuntimeError(f"{tensor_name} shape must have at least one dimension. "
                           "Make sure infer_shapes() was called previously.")
    input_shape = tuple(None if el.dim_param else el.dim_value for el in tensor_shape)
    assert all(dim for dim in input_shape[1:]), "Only the first dim could be null."
    return input_shape


def get_tensor_dtype(tensor_name, graph):
    """Helper to read the type of one tensor.

    Args:
        tensor_name (str): the tensor to read the type.
        graph (GraphProto): the graph containing the tensor.

    Returns:
        np.dtype: the tensor type
    """
    node_info = get_tensor_value_info(tensor_name, graph)
    return onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[node_info.type.tensor_type.elem_type]


def array_to_tp(**kwargs):
    """Transform a numpy array list to TensorProto list
    Args:
        kwargs (dict, optional): a list of numpy arrays. Defaults to {}.
    Returns:
        list of TensorProto: the list of tensor proto.
    """
    # Transform each input in a TensorProto
    tensors = []
    for name, x in kwargs.items():
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        tensors.append(np_onnx.from_array(x, name))
    return tensors


def nodes_to_ops_list(nodes):
    """Helper to convert a list of nodes to a list of op types.

    Args:
        nodes (list of NodeProto): list of nodes.

    Returns:
        list of str: list of op types.
    """
    return [node.op_type for node in nodes]


def get_node(nodes, op_type):
    """Helper to get a node of a specific type.

    Args:
        nodes (list of NodeProto): list of nodes.
        op_type (str): the type of the node to get.

    Returns:
        NodeProto: the node if found, None otherwise.
    """
    filtered_ops = [node for node in nodes if node.op_type == op_type]
    if len(filtered_ops) != 1:
        # Return None if not found or too many
        return None
    return filtered_ops[0]


def get_next_neighbor_nodes(node, graph):
    """Retrieve the nodes that are connected to the input node.

    Args:
        node (NodeProto): the node to get the neighbors.
        graph (GraphProto): the graph containing the node.

    Returns:
        list of NodeProto: the list of neighbors.
    """
    # Get the nodes connected to the outputs
    input_nodes = []
    for target_node in graph.node:
        for target_input in target_node.input:
            if target_input in node.output:
                input_nodes.append(target_node)
    return input_nodes


def get_field(node, name: str, default=None):
    """Helper to get the value of a field of a node.

    Args:
        node (NodeProto): the node to read the field.
        name (str): the name of the field.
        default (Any, optional): if the field is not found, return this value.
            If not provided, raise an exception if not field. Defaults to None.

    Returns:
        the value of the field as np.array.
    """
    attr = find_by_name(name, node.attribute)
    if attr is None:
        assert default is not None, f"Node {node.name} does not have attribute {name}."
        # onnx.helper.get_attribute_value converts any iterable into a list
        if hasattr(default, "__iter__"):
            default = list(default)
        return default
    value = onnx.helper.get_attribute_value(attr)
    if isinstance(value, onnx.TensorProto):
        # Convert value into an array when is a TensorProto
        value = np_onnx.to_array(value)
    elif isinstance(value, bytes):
        value = value.decode()
    return value


def get_variable(name, graph):
    """Helper to get the value of an initializar as np.array.

    Args:
        name (str): the name of the variable.
        graph (GraphProto): the graph containing the variable.

    Returns:
        np.array: the value of the variable.
    """
    initializer = find_by_name(name, graph.initializer)
    return onnx.numpy_helper.to_array(initializer)


def to_field(name, value):
    """Helper to convert a value into an AttributeProto.

    Args:
        name (str): the attribute name.
        value (Any): the attribute value.

    Returns:
        AttributeProto: the attribute
    """
    if not isinstance(value, onnx.AttributeProto):
        # Convert any numpy array into a ProtoTensor
        if isinstance(value, np.ndarray):
            value = np_onnx.from_array(value)
        value = make_attribute(name, value)
    else:
        # Try to read the value to know if it is a valid attribute
        onnx.helper.get_attribute_value(value)
        # And verify name is correct
        assert value.name == name
    return value


def replace_field(node, attr_name, new_value):
    """Helper to replace the value of one attribute in a node by another.

    Args:
        node (NodeProto): the node.
        attr_name (str): the attribute name of the value to be replaced.
        new_value (Any): the new value.
    """
    # We replace field only if types are the same
    node_attr = get_field(node, attr_name)
    if type(new_value) != type(node_attr):
        raise ValueError("Impossible to replace attributes. "
                         f"Expected {type(node_attr)} value type.")
    # Convert new value into an attribute
    new_value_attr = to_field(attr_name, new_value)

    # Search and replace attribute in node
    set_by_name(attr_name, node.attribute, new_value_attr)


def infer_partial_io(nodes, exclude=[]):
    """Infer the partial inputs/outputs for a list of 'connected' nodes.

    Args:
        nodes (list of NodeProto): the nodes list.
        exclude (list of str): exclude tensors with these names. Defaults to [].

    Returns:
        list, list: the inputs outputs infered.
    """
    # Search partial outputs
    def _extract_unique_not_null_elems(elems, exclude=[]):
        return sorted(set(el for el in elems if el not in exclude and el), key=elems.index)

    # Infer ordered, not null and unique input/output names
    all_inputs = sum([list(node.input) for node in nodes], [])
    all_outputs = sum([list(node.output) for node in nodes], [])
    inputs = _extract_unique_not_null_elems(all_inputs, exclude=all_outputs + exclude)
    outputs = _extract_unique_not_null_elems(all_outputs, exclude=all_inputs + exclude)
    return inputs, outputs
