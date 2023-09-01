import sys
import copy
import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from onnx2tf.utils.common_functions import (
    get_constant_or_variable,
    print_node_info,
    inverted_operation_enable_disable,
    make_tf_node_info,
    get_replacement_parameter,
    pre_process_transpose,
    post_process_transpose,
)


@print_node_info
@inverted_operation_enable_disable
@get_replacement_parameter
def make_node(
    *,
    graph_node: gs.Node,
    tf_layers_dict: dict,
    **kwargs: dict,
):
    """Pad

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    before_op_output_shape_trans = True
    if len(graph_node.inputs) == 1:
        before_op_output_shape_trans_1 = \
            tf_layers_dict.get(graph_node.inputs[0].name, {}).get('before_op_output_shape_trans', True)
        before_op_output_shape_trans = \
            before_op_output_shape_trans_1
    elif len(graph_node.inputs) >= 2:
        before_op_output_shape_trans_1 = \
            tf_layers_dict.get(graph_node.inputs[0].name, {}).get('before_op_output_shape_trans', True)
        before_op_output_shape_trans_2 = \
            tf_layers_dict.get(graph_node.inputs[1].name, {}).get('before_op_output_shape_trans', True)
        before_op_output_shape_trans = \
            before_op_output_shape_trans_1 \
            and before_op_output_shape_trans_2

    graph_node_input = get_constant_or_variable(
        graph_node.inputs[0],
        before_op_output_shape_trans,
    )

    constant_value = 0
    if len(graph_node.inputs) >= 3  and graph_node.inputs[2].name != '':
        constant_value = get_constant_or_variable(
            graph_node.inputs[2],
            before_op_output_shape_trans,
        )
    graph_node_output: gs.Variable = graph_node.outputs[0]
    shape = graph_node_output.shape
    dtype = graph_node_output.dtype

    input_tensor = tf_layers_dict[graph_node_input.name]['tf_node'] \
        if isinstance(graph_node_input, gs.Variable) else graph_node_input
    tensor_rank = len(input_tensor.shape)

    # Pre-process transpose
    input_tensor = pre_process_transpose(
        value_before_transpose=input_tensor,
        param_target='inputs',
        param_name=graph_node.inputs[0].name,
        **kwargs,
    )

    constant_value = tf_layers_dict[constant_value.name]['tf_node'] \
        if isinstance(constant_value, gs.Variable) else constant_value

    # Transpose pads values
    paddings = None
    if len(graph_node.inputs) >= 2:
        paddings = get_constant_or_variable(
            graph_node.inputs[1],
            False,
        )
        paddings = tf_layers_dict[paddings.name]['tf_node'] \
            if isinstance(paddings, gs.Variable) else paddings
    paddings = graph_node.attrs.get('pads', paddings)
    if isinstance(paddings, list):
        paddings = np.asarray(paddings)

    values = None
    if hasattr(paddings, 'values'):
        values = paddings.values
    elif isinstance(paddings, np.ndarray):
        values = paddings
    elif hasattr(paddings, 'numpy'):
        values = paddings.numpy()

    if values is not None:
        paddings = values.reshape([2, tensor_rank]).transpose()
        paddings_rank = paddings.shape[0]
        if paddings_rank > 2:
            """
            onnx paddings:
                [
                    dim0_begin,
                    dim1_begin,
                    dim2_begin,
                    dim3_begin,
                        :
                    dim0_end,
                    dim1_end,
                    dim2_end,
                    dim3_end,
                        :
                ]

                e.g.
                Tensor:
                    [1,128,128,3]
                paddings:
                    [5,3,1,0,4,2,0,0]
                Result:
                    [10,133,129,3]

            tf paddings:
                [
                    [dim0_begin, dim0_end],
                    [dim1_begin, dim1_end],
                    [dim2_begin, dim2_end],
                    [dim3_begin, dim3_end],
                            :
                ]

                e.g.
                Tensor:
                    [1,128,128,3]
                paddings:
                    [
                        [5,4], ... dim=0, begin_pad=5, end_pad=4
                        [3,2], ... dim=1, begin_pad=3, end_pad=2
                        [1,0], ... dim=2, begin_pad=1, end_pad=0
                        [0,0], ... dim=3, begin_pad=0, end_pad=0
                    ]
                Result:
                    [10,133,129,3]
            """
            paddings = np.asarray(
                [[begin, end] \
                    for begin, end in zip(values[0:tensor_rank:1], values[tensor_rank:tensor_rank+tensor_rank:1])],
                dtype=values.dtype,
            )
            if before_op_output_shape_trans:
                convertion_table = [0] + [i for i in range(2, tensor_rank)] + [1]
                new_values = [0] * tensor_rank
                for new_idx, idx in enumerate(convertion_table):
                    new_values[new_idx] = paddings[idx]
                paddings = np.asarray(new_values, dtype=paddings.dtype)
            paddings = tf.convert_to_tensor(paddings) \
                if isinstance(paddings, np.ndarray) else paddings

    elif tf.keras.backend.is_keras_tensor(paddings):
        paddings = \
            tf.transpose(
                a=tf.reshape(
                    tensor=paddings,
                    shape=[2, tensor_rank]
                )
            )
        paddings_rank = paddings.shape[0]
        if paddings_rank > 2:
            paddings = [
                [begin, end] \
                    for begin, end in paddings
            ]
            if before_op_output_shape_trans:
                convertion_table = [0] + [i for i in range(2, tensor_rank)] + [1]
                new_values = [0] * tensor_rank
                for new_idx, idx in enumerate(convertion_table):
                    new_values[new_idx] = paddings[idx]
                paddings = new_values

    mode = graph_node.attrs.get('mode', 'constant')

    # Preserving Graph Structure (Dict)
    tf_layers_dict[graph_node_output.name] = {
        'optype': graph_node.op,
        'shape': shape,
        'dtype': dtype,
        'nhwc': tf_layers_dict[graph_node_input.name]['nhwc'] \
            if isinstance(graph_node_input, gs.Variable) \
                and 'nhwc' in tf_layers_dict[graph_node_input.name].keys() else False
    }

    # Generation of TF OP
    # Workaround for problem with TFLite runtime outputting anomalous values with INT64 padding specification
    # https://github.com/PINTO0309/onnx2tf/issues/351
    if isinstance(paddings, np.ndarray):
        paddings = tf.cast(tf.convert_to_tensor(paddings), dtype=tf.int32)
    else:
        paddings = tf.cast(paddings, dtype=tf.int32)

    if mode != 'edge':
        # mode != 'edge'
        tf_layers_dict[graph_node_output.name]['tf_node'] = \
            tf.pad(
                tensor=input_tensor,
                paddings=paddings,
                mode=mode,
                constant_values=constant_value,
                name=graph_node.name,
            )
    else:
        # mode = 'edge'
        input_tensor_padded = input_tensor
        for idx, p in enumerate(paddings):
            begin_, end_ = p[0], p[1]
            empty_paddings = np.zeros([tensor_rank, 2], dtype=np.int32)
            for idxe, empty_padding in enumerate(empty_paddings):
                if idxe == idx:
                    empty_padding[0], empty_padding[1] = begin_, end_
                else:
                    pass
            if (empty_paddings == 0).all() != True:
                # begin
                begin_loop_count = empty_paddings[idx][0]
                temp_empty_paddings = copy.deepcopy(empty_paddings)
                temp_empty_paddings[idx][0] = 1
                temp_empty_paddings[idx][1] = 0
                for _ in range(begin_loop_count):
                    input_tensor_padded = tf.pad(input_tensor_padded, temp_empty_paddings, 'SYMMETRIC')
                # end
                end_loop_count = empty_paddings[idx][1]
                temp_empty_paddings = copy.deepcopy(empty_paddings)
                temp_empty_paddings[idx][0] = 0
                temp_empty_paddings[idx][1] = 1
                for _ in range(end_loop_count):
                    input_tensor_padded = tf.pad(input_tensor_padded, temp_empty_paddings, 'SYMMETRIC')
        tf_layers_dict[graph_node_output.name]['tf_node'] = input_tensor_padded

    # Post-process transpose
    tf_layers_dict[graph_node_output.name]['tf_node'] = post_process_transpose(
        value_before_transpose=tf_layers_dict[graph_node_output.name]['tf_node'],
        param_target='outputs',
        param_name=graph_node.outputs[0].name,
        **kwargs,
    )

    # Generation of Debug Info
    tf_layers_dict[graph_node_output.name]['tf_node_info'] = \
        make_tf_node_info(
            node_info={
                'tf_op_type': 'Pad',
                'tf_inputs': {
                    'x': input_tensor,
                    'paddings': paddings,
                    'constant_value': constant_value,
                    'mode': mode,
                    'tensor_rank': tensor_rank,
                },
                'tf_outputs': {
                    'output': tf_layers_dict[graph_node_output.name]['tf_node'],
                },
            }
        )
