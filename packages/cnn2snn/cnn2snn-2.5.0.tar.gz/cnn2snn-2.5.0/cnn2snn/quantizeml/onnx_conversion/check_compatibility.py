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
__all__ = ["check_weight_types"]

import numpy as np
import akida

from .padding import compute_pads, compute_padding_out_shape


def check_input_dtype(converter):
    """Check that input tensor has the expected type.

    Args:
        converter (OnnxConverter): the converter.

    Raises:
        ValueError: if input tensor does not have the expected type.
    """
    compatible_dtypes = np.dtype("uint8") if converter.is_input_layer else np.dtype("int8")
    if converter.input_dtype != compatible_dtypes:
        raise ValueError(f"Expected an input dtype {compatible_dtypes} on {converter.name} node.")


def check_weight_types(converter, weight_names, expect_types):
    """Check that weights have the expected type.

    Args:
        converter (OnnxConverter): the converter.
        weight_names (list of str): list of weight names to check.
        expect_types (list of str): list of expected weight types.

    Raises:
        RuntimeError: if a weight does not exist.
        ValueError: if a weight does not have the expected type.
    """
    assert len(weight_names) == len(expect_types), "Expect to have same lenght of elements."

    weights = converter.weights
    for w_name, e_type in zip(weight_names, expect_types):
        if w_name not in weight_names:
            raise RuntimeError(f"{converter.name} was expected to have '{w_name}' weight.")
        w_dtype = weights[w_name].dtype
        if w_dtype != np.dtype(e_type):
            raise ValueError(f"{w_name} in {converter.name} must be {e_type} type, not {w_dtype}.")


def check_attributes(converter, attr_names):
    """Check that attributes were loaded into converter.

    Args:
        converter (OnnxConverter): the converter.
        weight_names (list of str): list of attribute names to check.

    Raises:
        RuntimeError: if an attribute does not exist.
    """
    for expect_attr in attr_names:
        if not hasattr(converter, expect_attr):
            raise RuntimeError(f"{converter.name} expect to have '{expect_attr}' attribute.")


def check_if_squared(value, name_val=None):
    """Check if input value is square.

    Args:
        value (object): the value to check.
        name_val (str, optional): name of the value. Defaults to None.

    Raises:
        ValueError: if value is not square.
    """
    assert hasattr(value, "__iter__")
    if name_val is None:
        name_val = str(value)
    if value[0] != value[1]:
        raise ValueError(f"{name_val} is expected to be square.")


def check_padding_compatibility(converter):
    """Check if pads are compatible with expected in akida.

    Args:
        converter (OnnxConverter): the converter.

    Raises:
        ValueError: When convolutional pads (or max pool pads) are not compatible with Akida.
    """

    is_same = converter.padding == akida.Padding.Same
    kernel_shapes = converter.weights["W"].shape[-2:]
    exp_pads = compute_pads(converter.input_shape, kernel_shapes, converter.strides, is_same)

    # Pads in FC dimensions have to be zero
    fc_pads = converter.pads[:2] + converter.pads[4:6]
    if any(fc_pads):
        raise ValueError(f"Unrecognized {converter.pads} pads in {converter.name}.")
    # Compare if convolutional padding produces same behavior than Akida
    convert_pads = converter.pads[2:4] + converter.pads[6:]
    if convert_pads != exp_pads:
        raise ValueError(f"Expect pads {exp_pads} (found {converter.pads}) in {converter.name}.")

    # Compare if max pool padding produces same behavior than Akida
    if converter.pool_type == akida.PoolType.Max:
        # Calculate convolutional output shape
        out_shape = compute_padding_out_shape(converter.input_shape,
                                              kernel_shapes,
                                              converter.strides,
                                              convert_pads)
        exp_pads = compute_pads(out_shape, converter.pool_size, converter.pool_strides, is_same)
        if converter.pool_pads != exp_pads:
            raise ValueError(f"Expect pads {exp_pads} (found {converter.pool_pads}) "
                             f"in {converter.name} maxpool.")
