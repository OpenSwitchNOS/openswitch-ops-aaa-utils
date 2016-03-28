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
OpenSwitch Test for CHAP wrong configuration.
"""


TOPOLOGY = """
#  +----------+
#  |  switch  |
#  +----------+

# Nodes
[type=openswitch name="OpenSwitch 1"] switch
"""


def test_chap03_wronconfiguration(topology, step):
    """
    Verify if the switch can save the basic configuration of CHAP and PAP
    """
    sw = topology.get('switch')
    assert sw is not None

    # Attempt to enable another option using the command
    step("Attempt to enable another option using the command")
    sw('configure terminal')
    rc = sw('aaa authentication login radius radius-auth mam')
    if "% Unknown command." not in rc:
        assert False, "FAILED - The option was configured"

    # Verify the options of the command
    step("Verify the option of the command")
    rc = sw('aaa authentication login radius radius-auth ?').split("\n")
    if len(rc) != 3:
        assert False, "FAILED - The command has invalid options"
    if "  chap  set CHAP Radius authentication" not in rc:
        assert False, "Failed - The CHAP option  was not displayed"
    if "  pap  set PAP Radius authentication" not in rc:
        assert False, "Failed - The PAP option was not displayed"
