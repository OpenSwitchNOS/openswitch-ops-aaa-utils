# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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

from time import sleep

TOPOLOGY = """
# +--------+         +--------+
# |        |eth0     |        |
# |  hs2   +---------+  ops1  |
# |        |     eth1|        |
# +--------+         +-+------+
#                      |eth0
#                      |
#                      |eth0
#                  +---+----+
#                  |        |
#                  |  hs1   |
#                  |        |
#                  +--------+

# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=oobmhost image="openswitch/tacacs_server:latest" name="Host 1"] hs1
[type=oobmhost image="openswitch/tacacs_server:latest" name="Host 2"] hs2

# Ports
[force_name=oobm] ops1:eth1
[force_name=oobm] ops1:eth0

# Links
ops1:eth0 -- hs1:eth0
ops1:eth1 -- hs2:eth0
"""

USER1 = "user1"
USER1_PASSWD = "user1"

def tacacs_add_server(dut, step):
    step('\n### === Running: Add tacacs+ servers === ###\n')
    vtysh_shell = dut.get_shell('vtysh')
    matches = ['#']
    cmd = "su netop"
    assert vtysh_shell.send_command(cmd, matches) is 0
    dut("configure terminal")
    dut("tacacs-server host 192.168.1.254 key tac_test")
    dut("tacacs-server host 192.168.1.253 key tac_test")
    dut("end")
    dump = dut("show running-config")
    lines = dump.splitlines()
    count = 0

    for line in lines:
        if "tacacs-server host 192.168.1.254" in line:
           count = count + 1
        if "tacacs-server host 192.168.1.253" in line:
           count = count + 1
    assert count == 2,\
           '\n### Adding tacacs servers test failed ###'

    step('\n### Add tacacs+ servers: success ###\n')


def tacacs_create_server_group(dut, step):
    step('\n### === Running: Create tacacs_plus group tac1, tac2 === ###\n')
    dut("configure terminal")
    dut("aaa group server tacacs_plus tac1")
    dut("server 192.168.1.254")
    dut("exit")
    dut("aaa group server tacacs_plus tac2")
    dut("server 192.168.1.253")
    dut("end")

    count = 0
    dump = dut("show running-config")
    lines = dump.splitlines()

    for line in lines:
        if "aaa group server tacacs_plus tac1" in line:
            count = count + 1
        if "server 192.168.1.254" in line:
            count = count + 1
        if "aaa group server tacacs_plus tac2" in line:
            count = count + 1
        if "server 192.168.1.253" in line:
            count = count + 1
    assert count == 4,\
            '\n### Create tacacs_plus group tac1,tac2 and add server test failed ###'

    step('\n### Create tacacs_plus group tac1,tac2 : success ###\n')


def set_tacacs_cmd_authorization_none(dut, step):
    step('\n### === Running : Set none as tacacs+ command authorization and test command authorization === ###\n')
    dut("configure terminal")
    dut("aaa authorization commands default none")
    dut("end")

    count = 0
    ''' now check the running config '''
    dump = dut("show running-config")
    lines = dump.splitlines()
    for line in lines:
        if ("aaa authorization commands default none" in line):
            count = count + 1
    assert count == 1,\
            '\n### set aaa authorization to none test failed ###'

    step('\n### Test 1 : Set none as tacacs+ command authorization and test command authorization : Success ###\n')

def set_tacacs_cmd_authorization_none_and_groups(dut, step):
    step('\n### === Run: Set tacacs+ groups and none as tacacs cmd authorization and test command authorization === ###\n')
    dut("configure terminal")
    dut("aaa authorization commands default group tac1 tac2 none")
    dut("end")

    count = 0
    ''' now check the running config '''
    dump = dut("show running-config")
    lines = dump.splitlines()
    for line in lines:
        if ("aaa authorization commands default group tac1 tac2 none" in line):
            count = count + 1
    assert count == 1,\
            '\n### set aaa authorization with groups and test authorization test failed ###'

    step('\n### Test 2: Set tacacs+ groups and none as tacacs authorization and test command authorization: success ###\n')

def set_aaa_authentication(dut, step):
    step('\n### === Running : Set tacacs+ authentication with groups so that remote user can login === ###\n')
    dut("configure terminal")
    dut("aaa authentication login default group tac2 local")
    dut("end")

    count = 0
    ''' now check the running config '''
    dump = dut("show running-config")
    lines = dump.splitlines()
    for line in lines:
        if ("aaa authentication login default group tac2 local" in line):
            count = count + 1
    assert count == 1,\
            '\n### set aaa authentication with groups test failed ###'

    step('\n###  set aaa authentication with groups so that remote user can login: success ###\n')

def set_unreachable_servers_and_test_cmd_author(dut, step):
    step('\n### === Running : set unreachable tacacs+ server and test cmd authorization === ###\n')
    dut("configure terminal")
    dut("tacacs-server host 1.1.1.1")
    dut("aaa group server tacacs_plus tac3")
    dut("server 1.1.1.1")
    dut("exit")
    dut("aaa authorization commands default group tac3")
    dut("end")

    count = 0
    ''' now check the running config '''
    dump = dut("show running-config")
    lines = dump.splitlines()
    for line in lines:
        if ("Cannot execute command. Could not connect to any TACACS+ servers." in line):
            count = count + 1
    assert count == 1,\
           '\n ### Failed to verify unreachable tacacs server test ###\n'

    step('\n### Test4: set unreachable tacacs+ server for tacacs+ cmd authorization and test cmd authorization: success ###\n')


def ssh_as_tacacs_remote_user_and_cmd_authorization(step, hs1, user, pwd):
    step("### === Running : ssh to switch as a remote tacacs+ user and test command authorization === ###\n")

    ssh_cmd = "ssh -F /dev/null -o StrictHostKeyChecking=no " + user + \
        "@192.168.1.1"
    matches = ['password:']
    bash_shell = hs1.get_shell('bash')
    assert bash_shell.send_command(ssh_cmd, matches) is 0
    matches = ['#']
    assert bash_shell.send_command(pwd, matches) is 0, "ssh" \
        " as new user failed."
    cmd = "show run"
    matches = ['Cannot execute command. Command not allowed.']
    assert bash_shell.send_command(cmd, matches) is 0, "### Login as unauthorized user" \
        " and test command authorization failed ###"

    step('\n### Test3: ssh to switch as a remote tacacs+ user and test command authorization: success ###\n')

def start_tacacs_service(step, host):
    step("#### Running : start tac_plus daemon on the server ####\n")
    out = host("service tac_plus start")
    assert ("Starting Tacacs+ server") in out, "Failed to start tac_plus on the host"
    step("### Started tacacs service on the tacacs server ###\n")

def test_tacacs_cmd_authorization_feature(topology, step):
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    # Wait switch to come up
    sleep(10)

    # Server IP address
    hs1.libs.ip.interface('eth0', addr='192.168.1.254/24', up=True)

    hs2.libs.ip.interface('eth0', addr='192.168.1.253/24', up=True)

    # Switch IP address
    with ops1.libs.vtysh.ConfigInterfaceMgmt() as ctx:
        ctx.ip_static('192.168.1.1/24')

    tacacs_add_server(ops1, step)

    tacacs_create_server_group(ops1, step)

    start_tacacs_service(step, hs1)
    start_tacacs_service(step, hs2)

    set_aaa_authentication(ops1, step)

    set_tacacs_cmd_authorization_none(ops1, step)

    set_tacacs_cmd_authorization_none_and_groups(ops1, step)

    ssh_as_tacacs_remote_user_and_cmd_authorization(step, hs1, USER1, USER1_PASSWD)

    set_unreachable_servers_and_test_cmd_author(ops1, step)

    step("\n\n### !!! All the tests for tacacs command authorization passed !!! ####\n")
