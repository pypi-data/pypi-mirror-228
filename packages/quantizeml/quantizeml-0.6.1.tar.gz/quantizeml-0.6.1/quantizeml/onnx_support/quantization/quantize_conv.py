import numpy as np
from onnx import numpy_helper as np_onnx
from ..layers.graph_tools import get_field, get_variable, get_node, array_to_tp, get_tensor_shape
from ..layers.conv2d import QuantizedConv2D
from ..layers.subgraph_ops.padding import transform_pads_into_array
from .weights import quantize_weights
from .input_scale import input_zp_scale
from .outputs import downscale
from .relu_max_value import quantize_relu_max_value


def conv_has_bias(conv_node):
    # If third attribute is there and it is not empty, then there is a bias
    if len(conv_node.input) == 3 and conv_node.input[2]:
        return True
    return False


def get_qconv(nodes):
    conv_node = nodes[0]
    assert conv_node.op_type == 'Conv'
    strides = get_field(conv_node, 'strides', (1, 1))

    pool_type = "none"
    pool_size = (2, 2)
    pool_strides = (1, 1)
    pool_node = get_node(nodes, 'MaxPool')
    pool_pads = [0, 0, 0, 0]
    if pool_node:
        pool_type = "max"
        # kernel_shape attribute is mandatory for MaxPool
        pool_size = get_field(pool_node, 'kernel_shape')
        pool_strides = get_field(pool_node, 'strides', pool_strides)
        pool_pads = get_field(pool_node, "pads", pool_pads)
    pool_node = get_node(nodes, 'GlobalAveragePool')
    if pool_node:
        pool_type = "gap"

    act_node = get_node(nodes, 'Relu')
    max_value = act_node and len(act_node.input) > 2 and act_node.input[2]
    use_bias = conv_has_bias(conv_node)

    qconv = QuantizedConv2D(strides=strides,
                            pool_type=pool_type,
                            pool_size=pool_size, pool_strides=pool_strides,
                            pool_pads=pool_pads,
                            activation=bool(act_node),
                            max_value=max_value,
                            use_bias=use_bias)
    return qconv


def conv_quantize_initializers(qconv, tensor_range, nodes, graph, i_scale,
                               zero_point=0):
    conv_node = nodes[0]

    kernel_name = conv_node.input[1]
    kernel = get_variable(kernel_name, graph)
    if kernel.dtype != np.float32:
        raise ValueError(f"Unexpected weights dtype {kernel.dtype} for layer " +
                         conv_node.name)

    bias_name = ""
    bias = 0
    use_bias = conv_has_bias(conv_node)
    if use_bias:
        bias_name = conv_node.input[2]
        bias = get_variable(bias_name, graph)
    elif zero_point != 0:
        raise ValueError(f"Expected a bias in {conv_node.name} because zero point is not zero.")

    # Perform cross-layer equalization, i.e.: rescale weights with input scale.
    # To do that first reshape i_scale to put last two dimensions to 1 and be
    # capable of broadcasting.
    i_scale = np.array(i_scale)
    assert i_scale.ndim <= 1
    i_scale = i_scale.reshape((-1, 1, 1))
    kernel = kernel / i_scale
    # Quantize and set weights and bias
    qweights, qbias, i_scale = quantize_weights(kernel, bias, zero_point)
    # Reshape scale to match with channel axis
    i_scale = i_scale.reshape((-1, 1, 1))

    # Prepare tensors list with unique names
    conv_name = conv_node.name
    prefix = conv_name + "_"
    weights_dict = {prefix + "Xpad": zero_point, prefix + "Wi": qweights}
    if use_bias:
        weights_dict[prefix + "B"] = qbias
    pads = get_field(conv_node, 'pads', (0, 0, 0, 0))
    weights_dict[prefix + "pads"] = transform_pads_into_array(pads)

    # Quantize max value when there is an activation
    qmax_value = quantize_relu_max_value(nodes, i_scale, graph)
    if qmax_value is not None:
        weights_dict[prefix + "max_value"] = qmax_value

    # Fold spatial dimension when GAP
    if "GlobalAvgPool" in qconv.op_type:
        input_shape = get_tensor_shape(conv_node.output[0], graph)
        i_scale *= input_shape[-2] * input_shape[-1]

    # Now consider calibrated output range
    scale, s_out, ocalib_scale = downscale(nodes[-1], tensor_range, i_scale, graph)
    weights_dict.update({prefix + "M": scale, prefix + "S_out": s_out})

    # Create node
    inputs = conv_node.input[:1] + list(weights_dict)
    qnode = qconv.make_node(inputs, nodes[-1].output, name=conv_name)
    onnx_weights = array_to_tp(**weights_dict)

    return qnode, ocalib_scale, onnx_weights


def conv_convert(nodes, tensor_range, graph, scales, _last_block):
    conv_node = nodes[0]
    input_name = conv_node.input[0]
    i_scale = scales.get(input_name, None)
    if i_scale is None:
        i_scale, zero_point = input_zp_scale(input_name, tensor_range, graph)
        if zero_point != 0 and not conv_has_bias(conv_node):
            # Zero point has to be folded into bias. If there is not bias,
            # we create a new one.
            kernel_name = conv_node.input[1]
            kernel_shape = get_variable(kernel_name, graph).shape
            bias = np.zeros(kernel_shape[0], "float32")
            bias_name = kernel_name + "_bias"
            conv_node.input.insert(2, bias_name)
            graph.initializer.append(np_onnx.from_array(bias, bias_name))
    else:
        zero_point = np.array(0, dtype=np.uint8)

    # A signed zero point is expected at conversion
    zero_point = np.array(zero_point, dtype=np.uint8)

    qconv = get_qconv(nodes)

    return conv_quantize_initializers(qconv, tensor_range,
                                      nodes, graph, i_scale, zero_point)
