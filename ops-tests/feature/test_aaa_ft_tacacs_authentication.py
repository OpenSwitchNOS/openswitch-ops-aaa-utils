# -*- coding: utf-8 -*-
# (C) Copyright 2015 Hewlett Packard Enterprise Development LP
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
OpenSwitch Test for vlan related configurations.
"""

from time import sleep
from pytest import mark
import pexpect
from pdb import set_trace

TOPOLOGY = """
# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=oobmhost image="openswitch/tacacs_server:latest" name="Host 1"] hs1

# Ports
[force_name=oobm] ops1:sp1

# Links
ops1:sp1 -- hs1:if01
"""


sshclient = "/usr/bin/ssh -q -o UserKnownHostsFile=/dev/null" \
    "  -o StrictHostKeyChecking=no"

switches = []
hosts = []

def setuptacacsserver(step):
    """ This function is to setup tacacs server
    """
    h1 = hosts[0]
    switchip = getswitchip(step)
    hostip = gethostip_1(step)

    step(".###hostIP: " + hostip + " ###\n")
    print("SwitchIP:" + switchip)
    print("hostIP:" + hostip)

    h1("service tac_plus start")
    sleep(2)
    out = h1("service tac_plus start ")
    assert ("fail") not in out, "Failed to start freeradius on host"

    step("################ Configured tacacs server ################ \n")


def getswitchip(step):
    """ This function is to get switch IP addess
    """
    s1 = switches[0]
    out = s1("ifconfig eth0", shell="bash")
    switchipaddress = out.split("\n")[1].split()[1][5:]
    return switchipaddress



def gethostip_1(step):
    """ This function is to get host IP addess
    """
    h1 = hosts[0]
    out = h1("ifconfig %s" % h1.ports["if01"])
    host_1_ipaddress = out.split("\n")[1].split()[1][5:]
    return host_1_ipaddress


def configure_tacacs_group(step, chap=False):
    """ This function is to enable radius authentication in DB
    with CLI command"""
    s1 = switches[0]

    out = ""
    out += s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    if chap:
        out += s1("echo ", shell="bash")
        out = s1("aaa authentication login default group tacacs_plus")
        assert "Unknown command" not in out, \
            "Failed to set chap for radius"
    else:
        out += s1("echo ", shell="bash")
        out = s1("aaa authentication login default group tacacs_plus")
        assert "Unknown command" not in out, "Failed to enable radius " \
            "authentication"

    out += s1("echo ", shell="bash")
    s1("exit")
    return True


def configure_tacacs_server(step):
    """ This function is to disable fallback to local in DB
    with CLI command"""
    s1 = switches[0]

    out = ""
    out += s1("echo ", shell="bash")
    out = s1("configure terminal")
    assert "Unknown command" not in out, \
        "Failed to enter configuration terminal"

    out += s1("echo ", shell="bash")
    gethostip_1_str = gethostip_1(step)
    out = s1("tacacs-server host " + gethostip_1_str +  " key tac_test")
    assert "Unknown command" not in out, \
        "unable to configure tacacs-server"

    out += s1("echo ", shell="bash")
    s1("exit")
    #set_trace()
    return True

def loginsshradius(step, chap=False):
    """This function is to verify radius authentication is successful when
    radius is true and fallback is false"""
    step("########## Test to verify SSH login with radius authentication "
         "enabled and fallback disabled ##########\n")
    s1 = switches[0]
    configure_tacacs_server(step)
    sleep(7)
    configure_tacacs_group(chap)
    sleep(7)
    ssh_newkey = "Are you sure you want to continue connecting"
    switchipaddress = getswitchip(step)
    step(".###switchIpAddress: " + switchipaddress + " ###\n")
    step(".### Running configuration ###\n")
    run = s1("show running-config")
    print(run)

    out = ""
    out += s1("echo ", shell="bash")
    myssh = sshclient + " bob@" + switchipaddress
    p = pexpect.spawn(myssh)

    i = p.expect([ssh_newkey, "password:", pexpect.EOF])

    if i == 0:
        p.sendline("yes")
        i = p.expect([ssh_newkey, "password:", pexpect.EOF])
    if i == 1:
        p.sendline("test")
    elif i == 2:
        assert i != 2, "Failed with SSH command"
    loginpass = p.expect(["password:", "#"])
    if loginpass == 0:
        p.sendline("dummypassword")
        p.expect("password:")
        p.sendline("dummypasswordagain")
        p.kill(0)
        assert loginpass != 0, "Failed to login via radius authentication"
    if loginpass == 1:
        p.sendline("exit")
        p.kill(0)
        if chap:
            step(".### Passed SSH login with radius authentication and"
                 " chap ###\n")
        else:
            step(".### Passed SSH login with radius authentication ###\n")
        return True


@mark.platform_incompatible(['ostl'])
def test_aaa_ft_authentication(topology, step):
    global switches, hosts
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')

    assert ops1 is not None
    assert hs1 is not None

    switches = [ops1]
    hosts = [hs1]

    ops1.name = "ops1"
    hs1.name = "hs1"

    setuptacacsserver(step)
    loginsshradius(step)
