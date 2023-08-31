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


def get_serialized_op_name(op_name,
                           use_bias=False,
                           pool_type=None,
                           activation=False,
                           max_value=False,
                           flatten=False,
                           scale=True):
    """Return the op_name with the right suffix given the parameter set.

    Args:
        op_name (str): the base operation name.
        use_bias (bool, optional): whether to append "Biased" as suffix. Defaults to False.
        pool_type (str, optional): the pool type to append as suffix. Defaults to None.
        activation (bool, optional): whether to append "ReLU" as suffix. Defaults to False.
        max_value (bool, optional): whether activation should have a max_value.
            Append "Clipped" as suffix. Defaults to False.
        flatten (bool, optional): whether to append "Flatten" as suffix. Defaults to False.
        scale (bool, optional): whether to append "Scaled" as suffix. Defaults to True.

    Returns:
        str: the operation name with suffixes.
    """
    if flatten:
        op_name += "Flatten"
    if use_bias:
        op_name += "Biased"
    if pool_type == "max":
        op_name += "MaxPool"
    if pool_type == "gap":
        op_name += "GlobalAvgPool"
    if activation:
        op_name += "ReLU"
        if max_value:
            op_name += "Clipped"
    if scale:
        op_name += "Scaled"
    return op_name
