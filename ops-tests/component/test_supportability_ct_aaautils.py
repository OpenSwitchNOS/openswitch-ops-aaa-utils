# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
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

TOPOLOGY = """
#
# +-------+
# |  sw1  |
# +-------+
#

# Nodes
[type=openswitch name="Switch 1"] sw1
"""


def check_aaa_daemon_diag(sw1, daemon, feature):
    # Variables
    str_check = 'diag-dump feature for AAA is not implemented'
    vtysh_cmd = 'diag-dump ' + feature + ' basic'
    tc_desc = vtysh_cmd + ' test '

    print("\n############################################")
    print("1.1 Running Diagnostic test for AAA. " + tc_desc)
    print("############################################\n")

    shell_cmd = "cp /etc/openswitch/supportability/ops_featuremapping.yaml\
     /etc/openswitch/supportability/ops_featuremapping.yaml2 "
    sw1(shell_cmd, shell="bash")

    shell_cmd = 'printf \'\n  -\n    feature_name: \"' + feature + \
        '\"\n    feature_desc: \"AAA feature Sample\"\n' + \
        '    daemon:\n     - \"' + daemon + '\"    ' + ' \' ' + \
        ' > /etc/openswitch/supportability/ops_featuremapping.yaml'

    sw1(shell_cmd, shell="bash")

    out = sw1(vtysh_cmd)

    shell_cmd = "mv /etc/openswitch/supportability/ops_featuremapping.yaml2\
     /etc/openswitch/supportability/ops_featuremapping.yaml "
    sw1(shell_cmd, shell="bash")

    assert str_check in out


def test_diag_dump(topology, step):
    sw1 = topology.get('sw1')

    assert sw1 is not None

    check_aaa_daemon_diag(sw1, 'ops_aaautilspamcfg', 'ops-aaa')
