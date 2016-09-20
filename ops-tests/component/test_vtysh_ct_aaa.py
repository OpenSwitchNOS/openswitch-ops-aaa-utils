# -*- coding: utf-8 -*-
# (C) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
##########################################################################

"""
OpenSwitch Test for switchd related configurations.
"""

# from pytest import set_trace
# from time import sleep
from pytest import mark

TOPOLOGY = """
# +-------+
# |  ops1 |
# +-------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
"""


def enablepasskeyauth(dut):
    ''' This function is to enable passkey authentication for
    SSH authentication method'''

    out = dut('configure terminal')
    assert 'Unknown command' not in out

    out = dut('ssh password-authentication')
    assert 'Command failed' not in out

    dut('end')

    out = dut('cat /etc/ssh/sshd_config', shell='bash')
    lines = out.splitlines()
    for line in lines:
        if 'PasswordAuthentication yes' in line:
            return True
    assert 'PasswordAuthentication yes' in out, \
        'Failed to enable password authentication'


def disablepasskeyauth(dut):
    ''' This function is to enable passkey authentication for
    SSH authentication method'''

    out = dut('configure terminal')
    assert 'Unknown command' not in out, \
        'Failed to enter configuration terminal'

    out = dut('no ssh password-authentication')
    assert 'Command failed' not in out, \
        'Failed to execute no ssh password authentication command'

    dut('end')

    out = dut('cat /etc/ssh/sshd_config', shell='bash')
    lines = out.splitlines()
    for line in lines:
        if 'PasswordAuthentication no' in line:
            return True
    assert 'PasswordAuthentication no' in out, \
        'Failed to disable password key authentication'


def enablepublickeyauth(dut):
    ''' This function is to enable passkey authentication for
    SSH authentication method'''

    out = dut('configure terminal')
    assert 'Unknown command' not in out, \
        'Failed to enter configuration terminal'

    out = dut('ssh public-key-authentication')
    assert 'Command failed' not in out, \
        'Failed to execute ssh public-key authentication command'

    dut('end')

    out = dut('cat /etc/ssh/sshd_config', shell='bash')
    lines = out.splitlines()
    for line in lines:
        if 'PubkeyAuthentication yes' in line:
            return True
    assert 'PubkeyAuthentication yes' in out, \
        'Failed to enable public key authentication'


def disablepublickeyauth(dut):
    ''' This function is to enable passkey authentication for
    SSH authentication method'''

    out = dut('configure terminal')
    assert 'Unknown command' not in out, \
        'Failed to enter configuration terminal'

    out = dut('no ssh public-key-authentication')
    assert 'Command failed' not in out, \
        'Failed to execute ssh no public-key authentication command'

    dut('end')

    out = dut('cat /etc/ssh/sshd_config', shell='bash')
    lines = out.splitlines()
    for line in lines:
        if 'PubkeyAuthentication no' in line:
            return True
    assert 'PubkeyAuthentication no' in out, \
        'Failed to disable public key authentication'

@mark.gate
@mark.skipif(True, reason="Will be enabled once RADIUS enhancements are ready")
def test_vtysh_ct_aaa(topology, step):
    ops1 = topology.get('ops1')
    assert ops1 is not None

    step('Test to enable SSH password authentication')
    enablepasskeyauth(ops1)

    step('Test to disable SSH password authentication')
    disablepasskeyauth(ops1)

    step('Test to enable SSH public key authentication')
    enablepublickeyauth(ops1)

    step('Test to disable SSH public key authentication')
    disablepublickeyauth(ops1)
