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
__all__ = ["Conv2DOnnxConverter"]

import numpy as np

import akida

from .base_converter import OnnxConverter
from .register import register_onnx_converter_target
from .conv_commons import check_convolution_compatibility, set_convolutional_variables


@register_onnx_converter_target("QuantizedConv2D")
class Conv2DOnnxConverter(OnnxConverter):
    """Convert QuantizedConv2D type node into an akida.Conv2D or akida.InputConv2D.

    Args:
        node (NodeProto): the node to convert.
        model (ModelProto): the model that the node is.
    """
    @property
    def is_input_layer(self):
        # This node is InputConv under the conditions:
        # 1. is the first node
        # 2. input channels are 1 or 3
        # 3. input type is uint8.
        return self._node == self._model.graph.node[0] and self.input_shape[-1] in [1, 3] and \
            self.input_dtype == np.dtype("uint8")

    def load_attributes(self, node):
        # Load default attributes
        super().load_attributes(node)

        # Some attributes should infer from node.op_type
        n_op = node.op_type
        self.activation = "ReLU" in n_op
        if "GlobalAvgPool" in n_op:
            self.pool_type = akida.PoolType.Average
        elif "MaxPool" in n_op:
            self.pool_type = akida.PoolType.Max
        else:
            self.pool_type = akida.PoolType.NoPooling
        self.use_bias = "Biased" in n_op

        # Padding type is inferred from pads attribute
        self.pads = self.weights["pads"].tolist()
        self.padding = akida.Padding.Same if any(self.pads) else akida.Padding.Valid

    def _additional_checks(self):
        check_convolution_compatibility(self, use_pad_value=True)

    def _parse_akida_layer(self):
        # Parse common information
        layer_params = {
            "name": self.name,
            "activation": self.activation,
            "output_bits": 8,
            "filters": self.weights["W"].shape[0],
            "kernel_size": self.weights["W"].shape[-1],
            "padding": self.padding,
            "pool_type": self.pool_type,
            "kernel_stride": self.strides[0],
        }
        if self.pool_type == akida.PoolType.Max:
            layer_params["pool_size"] = self.pool_size[0]
            layer_params["pool_stride"] = self.pool_size[0]

        if self.is_input_layer:
            ak_layer = akida.InputConv2D(padding_value=int(self.weights["x_pad_value"]),
                                         input_shape=self.input_shape,
                                         **layer_params)
        else:
            ak_layer = akida.Conv2D(**layer_params)
        return ak_layer

    def _set_akida_variables(self, ak_layer):
        set_convolutional_variables(self, ak_layer)
