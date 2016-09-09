# -*- coding: utf-8 -*-
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
#
##########################################################################

"""
OpenSwitch Test for TACACS+ Authentication.
"""

from time import sleep
from pytest import mark
import pexpect

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


ssh_client = "/usr/bin/ssh -q -o UserKnownHostsFile=/dev/null" \
    "  -o StrictHostKeyChecking=no"

switches = []
hosts = []
USER_1 = "user1"
USER_NEW = "mario"

def setup_tacacs_server(step, new_user, new_pass):
    """ This function is to setup tacacs server
    """
    h1 = hosts[0]
    h2 = hosts[1]
    host_ip = get_host_ip(step, 1)
    step("####### Configure TACACS+ servers start #######")
    step("#### Stop tac_plus daemon for servers ####")
    h1("service tac_plus stop")
    h2("service tac_plus stop")

    sleep(2)
    step("#### Add user " + new_user + " to host " + host_ip + "  ####")
    content = "\nuser = " + new_user + " {\n        pap = cleartext " + new_pass + "\n        service = exec {\n         priv-lvl = 15\n        }\n}"

    out = h2("echo $\'" + content + "\' >> /etc/tacacs/tac_plus.conf")
    out = h2("cat /etc/tacacs/tac_plus.conf")
    print(out)
    assert (content) in out, "Failed to add user"
    step("#### Restart tac_plus daemon for servers ####")
    out = h1("service tac_plus start")
    assert ("fail") not in out, "Failed to start tac_plus on host 1"
    out = h2("service tac_plus start")
    assert ("fail") not in out, "Failed to start tac_plus on host 2"

    step("####### Configure TACACS+ servers succeed #######")


def setup_tacacs_client(step):
    """ This function is to setup TACACS+ client in the switch
    """
    step("####### Configure TACACS+ client (on OpenSwitch) start #######")
    s1 = switches[0]
    host_1_ip_address = get_host_ip(step, 0)
    host_2_ip_address = get_host_ip(step, 1)
    print("TACACS+ Server:" + host_1_ip_address)
    print("TACACS+ Server:" + host_2_ip_address)
    sleep(2)
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    sleep(2)
    s1("tacacs-server host " + host_1_ip_address + " key tac_test")
    s1("tacacs-server host " + host_2_ip_address + " key tac_test")
    s1("aaa group server tacacs+ sg1")
    s1("server " + host_1_ip_address)
    s1("exit")
    s1("aaa group server tacacs+ sg2")
    s1("server " + host_2_ip_address)
    s1("end")
    step("####### Configure TACACS+ client (on OpenSwitch) succeed #######")


def get_switch_ip(step):
    """ This function is to get switch IP addess
    """
    s1 = switches[0]
    out = s1("ifconfig eth0", shell="bash")
    switch_ip = out.split("\n")[1].split()[1][5:]
    return switch_ip


def get_host_ip(step, host_id):
    """ This function is to get host IP addess
    """
    host = hosts[host_id]
    out = host("ifconfig %s" % host.ports["eth0"])
    host_ip_address = out.split("\n")[1].split()[1][5:]
    return host_ip_address


def enable_local_authentication(step):
    """ This function is to enable local authentication in DB
    with CLI command"""
    step("####### Configure local authentication  #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("aaa authentication login default local")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default local" in out, \
        "Failed to configure aaa authentication local"

def enable_tacacs_authentication_by_group(step):
    """ This function is to enable TACACS+ authentication in DB
    with CLI command"""
    step("####### Configure TACACS+ authentication  #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("aaa authentication login default group sg1 sg2")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default group sg1 sg2" in out, \
        "Failed to configure aaa authentication by server group sg1 sg2"

def disable_authentication_by_group(step):
    """ This function is to disable group authentication in DB
    with CLI command"""
    step("####### Configure authentication disable (default local authentication)  #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("no aaa authentication login default")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default" not in out, \
        "Failed to disable aaa authentication"

def enable_tacacs_authentication_by_group_local_first(step):
    """ This function is to enable TACACS+ authentication in DB
    with CLI command"""
    step("####### Configure TACACS+ authentication by group local first #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("aaa authentication login default group local sg1 sg2")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default group local sg1 sg2" in out, \
        "Failed to configure aaa authentication by server group local sg1 sg2"

def enable_tacacs_authentication_by_group_local_middle(step):
    """ This function is to enable TACACS+ authentication in DB
    with CLI command"""
    step("####### Configure TACACS+ authentication by group local in between #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("aaa authentication login default group sg1 local sg2")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default group sg1 local sg2" in out, \
        "Failed to configure aaa authentication by server group sg1 local sg2"

def enable_tacacs_authentication_by_group_local_last(step):
    """ This function is to enable TACACS+ authentication in DB
    with CLI command"""
    step("####### Configure TACACS+ authentication by group local last #######")
    s1 = switches[0]
    out = s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    s1("aaa authentication login default group sg1 sg2 local")
    s1("exit")

    out = s1("show running-config")
    assert "aaa authentication login default group sg1 sg2 local" in out, \
        "Failed to configure aaa authentication by server group sg1 sg2 local"

def login_ssh_local(step):
    """This function is to verify local authentication is successful
     """
    step("####### Test SSH login with local authenication start #######")
    s1 = switches[0]
    ssh_newkey = "Are you sure you want to continue connecting"
    switch_ip = get_switch_ip(step)
    step("#### Switch ip address: " + switch_ip + " ####")
    step("#### Running configuration ####")
    run = s1("show running-config")
    print(run)
    out = s1("echo ", shell="bash")
    myssh = ssh_client + " netop@" + switch_ip
    p = pexpect.spawn(myssh)

    address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])

    if address_known == 0:
        p.sendline("yes")
        address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 1:
        p.sendline("netop")
        remote_auth = p.expect(["#", "password:"])
        if remote_auth == 0:
            p.sendline("exit")
            p.kill(0)
            step("#### passed SSH login with local credenticals ####")
            return True
        elif remote_auth == 1:
            p.sendline("dummypassword")
            p.expect("password:")
            p.sendline("dummypasswordagain")
            p.kill(0)
            assert remote_auth != 1, "Failed to authenticate with local password"
    assert address_known != 2, "Failed with SSH command"
    step("####### Test SSH login with local authenication succeed #######")



def login_ssh_tacacs(step, username, password):
    """This function is to verify TACACS+ authentication is successful
    """
    step("####### Test SSH login with TACACS+ authentication start #######")
    s1 = switches[0]
    ssh_newkey = "Are you sure you want to continue connecting"
    switch_ip = get_switch_ip(step)
    step("#### Switch ip address: " + switch_ip + " ####")
    step("#### Running configuration ####")
    run = s1("show running-config")
    print(run)
    out = s1("echo ", shell="bash")
    myssh = ssh_client + " " + username + "@" + switch_ip
    p = pexpect.spawn(myssh)

    address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 0:
        p.sendline("yes")
        address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 1:
        p.sendline(password)
    assert address_known != 2, "Failed with SSH command"
    login_pass = p.expect(["password:", "#"])
    if login_pass == 0:
        p.sendline("dummypassword")
        p.expect("password:")
        p.sendline("dummypasswordagain")
        p.kill(0)
        assert login_pass != 0, "Failed to login via TACACS+ authentication"
    if login_pass == 1:
        p.sendline("exit")
        p.kill(0)
    step("####### Test SSH login with TACACS+ authentication succeed #######")

def login_ssh_tacacs_fail_through(step, username, password):
    """This function is to verify TACACS+ authentication is successful
       when fail-through is enabled and user/password exist in second server
    """
    step("####### Test SSH login with TACACS+ authentication fail-through enable/disable start #######")
    s1 = switches[0]
    count = 0
    ssh_newkey = "Are you sure you want to continue connecting"
    switch_ip = get_switch_ip(step)
    step("##### test with no fail-through option start #####")
    step("#### Switch ip address: " + switch_ip + " ####")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"
    out = s1("no aaa authentication allow-fail-through")
    assert "Unknown command" not in out, \
        "Failed to disable aaa authentication allow-fail-through"
    s1("exit")
    step("#### Running configuration ####")
    run = s1("show running-config")
    print(run)
    out = s1("echo ", shell="bash")
    myssh = ssh_client + " " + username + "@" + switch_ip
    p = pexpect.spawn(myssh)

    address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 0:
        p.sendline("yes")
        address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 1:
        p.sendline(password)
    assert address_known != 2, "Failed with SSH command"
    login_pass = p.expect(["password:", "#"])
    if login_pass == 0:
        p.sendline("dummypassword")
        p.expect("password:")
        p.sendline("dummypasswordagain")
        p.kill(0)
        count = count + 1
    if login_pass == 1:
        p.sendline("exit")
        p.kill(0)
        assert login_pass == 1, "TACACS+ authentication bypassed"
    step("##### test with no fail-through option succeed #####")

    step("##### test with fail-through option start #####")
    step("#### Switch ip address: " + switch_ip + " ####")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"
    out = s1("aaa authentication allow-fail-through")
    assert "Unknown command" not in out, \
        "Failed to configure aaa authentication allow-fail-through"
    s1("exit")
    run = s1("show running-config")
    assert "aaa authentication allow-fail-through" in run, \
        "Failed to enable fail-through for authentication"

    step("#### Running configuration ####")
    print(run)
    out = s1("echo ", shell="bash")
    myssh = ssh_client + " " + username + "@" + switch_ip
    p = pexpect.spawn(myssh)

    address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 0:
        p.sendline("yes")
        address_known = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if address_known == 1:
        p.sendline(password)
    assert address_known != 2, "Failed with SSH command"
    login_pass = p.expect(["password:", "#"])
    if login_pass == 0:
        p.sendline("dummypassword")
        p.expect("password:")
        p.sendline("dummypasswordagain")
        p.kill(0)
        assert login_pass == 0, "TACACS+ authentication failed"
    if login_pass == 1:
        p.sendline("exit")
        p.kill(0)
        count = count + 1
    step("##### test with fail-through option succeed #####")
    assert count == 2, "fail-through enable/disable test failed"
    step("####### Test SSH login with TACACS+ authentication fail-through enable/disable succeed #######")


@mark.platform_incompatible(['ostl'])
def test_aaa_ft_authentication(topology, step):
    global switches, hosts
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert ops1 is not None
    assert hs1 is not None
    assert hs2 is not None

    switches = [ops1]
    hosts = [hs1, hs2]

    ops1.name = "ops1"
    hs1.name = "hs1"
    hs2.name = "hs2"

    setup_tacacs_server(step, USER_NEW, "super")
    setup_tacacs_client(step)

    enable_local_authentication(step)
    login_ssh_local(step)

    enable_tacacs_authentication_by_group(step)
    login_ssh_tacacs(step, USER_1, USER_1)
    login_ssh_tacacs_fail_through(step, USER_NEW, "super")

    enable_tacacs_authentication_by_group_local_first(step)
    login_ssh_local(step)

    enable_tacacs_authentication_by_group_local_middle(step)
    login_ssh_tacacs_fail_through(step, "netop", "netop")

    enable_tacacs_authentication_by_group_local_last(step)
    login_ssh_tacacs_fail_through(step, "netop", "netop")

    disable_authentication_by_group(step)
    login_ssh_local(step)
