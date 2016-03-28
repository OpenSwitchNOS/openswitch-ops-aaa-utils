# -*- coding: utf- -*-
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
OpenSwitch Test for Chap basic configuration.
"""


TOPOLOGY = """
#  +----------+
#  |  switch  |
#  +----------+

# Nodes
[type=openswitch name="OpenSwitch 1"] switch
"""


def test_chap01_basic(topology, step):
    """
    Verify if the switch can save the basic configuration of CHAP/PAP
    """
    sw = topology.get('switch')
    assert sw is not None

    # Configure PAP authentication
    step("Configure PAP authentication on swtich")
    sw('configure terminal')
    sw('aaa authentication login radius radius-auth pap')
    sw('exit')

    # Verify PAP configuration
    step("Verify PAP configuration")
    configuration = ('show running-configuration')
    if "aaa authentication login radius\\n" not in configuration:
        assert False, "Failed- Verify PAP authentication"

    # Configure CHAP authentication
    step("Configure CHAP authentication on swtich")
    sw('configure terminal')
    sw('aaa authentication login radius radius-auth chap')
    sw('exit')

    # Verify chap configuration
    step("Verify chap configuration")
    configuration = ('show running-configuration')
    if "aaa authentication login radius radius-auth chap" not in configuration:
        assert False, "Failed - Verify chap configuration"
