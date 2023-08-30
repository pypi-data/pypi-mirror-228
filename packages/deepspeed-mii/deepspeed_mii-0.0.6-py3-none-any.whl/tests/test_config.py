# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

import pytest
import pydantic

import mii


def test_base_config():
    config = {'port_number': 12345, 'tensor_parallel': 4}
    mii_config = mii.config.MIIConfig(**config)

    assert mii_config.port_number == config['port_number']
    assert mii_config.tensor_parallel == config['tensor_parallel']


@pytest.mark.parametrize("config",
                         [
                             {
                                 'port_number': 'fail',
                                 'tensor_parallel': 'fail'
                             },
                             {
                                 'port_number': 'fail',
                                 'tensor_parallel': 4
                             },
                             {
                                 'port_number': 12345,
                                 'tensor_parallel': 'fail'
                             },
                             {
                                 'port_fail': 12345,
                                 'tensor_parallel': 4
                             },
                         ])
def test_base_config_literalfail(config):
    with pytest.raises(pydantic.ValidationError):
        mii_config = mii.config.MIIConfig(**config)
