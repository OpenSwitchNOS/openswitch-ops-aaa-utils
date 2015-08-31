from smart import Error, _
from smart.util import pexpect

import os
import sys
import subprocess
from time import sleep
import pytest

from halonvsi.docker import *
from halonvsi.halon import *

def delay(sec=0.25):
    sleep(sec)

class myTopo(Topo):
    """Custom Topology Example
    H1[h1-eth0]<--->[1]S1[2]<--->H2[h2-eth0]
    """

    def build(self, hsts=2, sws=1, **_opts):
        self.hsts = hsts
        self.sws = sws

        "add list of hosts"
        for h in irange(1, hsts):
            host = self.addHost('h%s' % h)

        "add list of switches"
        for s in irange(1, sws):
            switch = self.addSwitch('s%s' % s)

        "Add links between nodes based on custom topo"
        self.addLink('h1', 's1')
        self.addLink('h2', 's1')

class aaaFeatureTest(HalonTest):
    def setupNet(self):
        # Create a topology with single Halon switch and
        # one host.

        # Select halon-host image from docker hub, which has freeradius
        # installed.
        self.setHostImageOpts("halon/halon-host")

        topo = myTopo(hsts = 2, sws = 1, hopts = self.getHostOpts(),
                      sopts = self.getSwitchOpts(), switch = HalonSwitch,
                      host = HalonHost, link = HalonLink, controller = None,
                      build = True)

        self.net = Mininet(topo, switch = HalonSwitch, host = HalonHost,
                           link = HalonLink, controller = None, build = True)

    def getSwitchIP(self):
        ''' This function is to get switch IP addess
        '''
        s1 = self.net.switches [ 0 ]
        out = s1.cmd("ifconfig eth0")
        switchIpAddress = out.split("\n")[1].split()[1][5:]
        return switchIpAddress

    def getHostIP_1(self):
        ''' This function is to get host IP addess
        '''
        h1 = self.net.hosts [ 0 ]
        out = h1.cmd("ifconfig eth0")
        host_1_IpAddress = out.split("\n")[1].split()[1][5:]
        return host_1_IpAddress

    def getHostIP_2(self):
        ''' This function is to get host IP addess
        '''
        h2 = self.net.hosts [ 1 ]
        out = h2.cmd("ifconfig eth0")
        host_2_IpAddress = out.split("\n")[1].split()[1][5:]
        return host_2_IpAddress

    # Call checkAccessFiles to verify if configurations files are modified
    # Update caller functions in test cases to debug.
    def checkAccessFiles(self):
        '''This function is to check if /etc/pam.d/common-*-access are modified
        based on the change in DB by cli
        '''
        s1 = self.net.switches [ 0 ]
        out = s1.cmd("cat /etc/pam.d/common-auth-access")
        lines = out.split('\n')
        for line in lines:
            if "auth" in line:
                print(line)
        print '\n'
        delay()
        out = s1.cmd("cat /etc/pam.d/common-account-access")
        lines = out.split('\n')
        for line in lines:
            if "account" in line:
                print(line)
        print '\n'
        delay()
        out = s1.cmd("cat /etc/pam.d/common-password-access")
        lines = out.split('\n')
        for line in lines:
            if "password" in line:
                print(line)
        print '\n'
        delay()
        out = s1.cmd("cat /etc/pam.d/common-session-access")
        lines = out.split('\n')
        for line in lines:
            if "session" in line:
                print(line)
        print '\n'

    def localAuthEnable(self):
        ''' This function is to enable local authentication in DB
        with CLI command'''
        s1 = self.net.switches [ 0 ]
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), "Failed to enter configuration terminal"

        out = s1.cmdCLI("aaa authentication login local")
        assert ('Unknown command' not in out), "Failed to enable local authentication"

        s1.cmdCLI("exit")
        return True

    def radiusAuthEnable(self):
        ''' This function is to enable radius authentication in DB
        with CLI command'''
        s1 = self.net.switches [ 0 ]

        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), "Failed to enter configuration terminal"

        out = s1.cmdCLI("aaa authentication login radius")
        assert ('Unknown command' not in out), "Failed to enable radius authentication"

        s1.cmdCLI("exit")
        return True

    def noFallbackEnable(self):
        ''' This function is to disable fallback to local in DB
        with CLI command'''
        s1 = self.net.switches [ 0 ]

        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), "Failed to enter configuration terminal"

        out = s1.cmdCLI("no aaa authentication login fallback error local")
        assert ('Unknown command' not in out), "Failed to disable fallback to local authentication"

        s1.cmdCLI("exit")
        return True

    def FallbackEnable(self):
        ''' This function is to enable fallback to local in DB
        with CLI command'''
        s1 = self.net.switches [ 0 ]

        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), "Failed to enter configuration terminal"

        out = s1.cmdCLI("aaa authentication login fallback error local")
        assert ('Unknown command' not in out), "Failed to enable fallback to local authentication"

        s1.cmdCLI("exit")
        return True

    def setupRadiusserver(self):
        ''' This function is to setup radius server in the ubuntu image we are referring to
        '''
        info('.########## Setup free radius freeradius ##########\n')
        h1 = self.net.hosts [ 0 ]
        hostIp_1_Address = self.getHostIP_1()
        out = h1.cmd("sed -i '76s/steve/admin/' /etc/freeradius/users")
        out = h1.cmd("sed -i '76s/#admin/admin/' /etc/freeradius/users")
        out = h1.cmd("sed -i '196s/192.168.0.0/"+hostIp_1_Address+"/' /etc/freeradius/clients.conf")
        out = h1.cmd("sed -i '196,199s/#//' /etc/freeradius/clients.conf")

        h1.cmd("service freeradius stop")
        sleep(1)
        out = h1.cmd("service freeradius start")

        h2 = self.net.hosts [ 1 ]
        hostIp_2_Address = self.getHostIP_2()
        out = h2.cmd("sed -i '76s/steve/admin/' /etc/freeradius/users")
        out = h2.cmd("sed -i '76s/#admin/admin/' /etc/freeradius/users")
        out = h2.cmd("sed -i '196s/192.168.0.0/"+hostIp_2_Address+"/' /etc/freeradius/clients.conf")
        out = h2.cmd("sed -i '196,199s/#//' /etc/freeradius/clients.conf")

        h2.cmd("service freeradius stop")
        sleep(1)
        out = h2.cmd("service freeradius start")
        info('.### Passed radius server configuration on host ###\n')

    def setupRadiusclient(self):
        ''' This function is to setup radius client in the switch
        '''
        info('########## Setup radius client in the switch ##########\n')
        s1 = self.net.switches [ 0 ]
        host_1_IpAddress = self.getHostIP_1()
        host_2_IpAddress = self.getHostIP_2()
        s1.cmd("mkdir /etc/raddb/")
        s1.cmd("touch /etc/raddb/server")
        sleep(1)
        out = s1.cmdCLI("configure terminal")
        assert ('Unknown command' not in out), "Failed to enter configuration terminal"

        sleep(1)
        s1.cmdCLI("radius-server host " + host_1_IpAddress)
        sleep(1)
        s1.cmdCLI("radius-server host " + host_2_IpAddress)
        sleep(2)
        s1.cmdCLI("radius-server timeout 1")
        sleep(2)
        s1.cmdCLI("radius-server retries 0")
        s1.cmdCLI("exit")
        info('.### Passed setting up radius configuration on switch ###\n')

    def loginSSHlocal(self):
        '''This function is to verify local authentication is successful when
        radius is false and fallback is true'''
        info('########## Test to verify SSH login with local authenication enabled ##########\n')
        s1 = self.net.switches [ 0 ]
        # self.checkAccessFiles()
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('admin')
            j = p.expect(['#', 'password:'])
            if j == 0:
                p.sendline('exit')
                p.kill(0)
                info(".### Passed SSH login with local credenticals ###\n")
                return True
            if j == 1:
                p.sendline('dummypassword')
                p.expect('password:')
                p.sendline('dummypasswordagain')
                p.kill(0)
                assert j <> 1, "Failed to authenticate with local password"
        elif i == 2:
            assert i <> 2, "Failed with SSH command"

    def loginSSHradius(self):
        '''This function is to verify radius authentication is successful when
        radius is true and fallback is false'''
        info('########## Test to verify SSH login with radius authenication enabled and fallback disabled ##########\n')
        s1 = self.net.switches [ 0 ]
        retFallback = self.noFallbackEnable()
        sleep(5)
        retAuth = self.radiusAuthEnable()
        sleep(5)
        # self.checkAccessFiles()
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('testing')
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('dummypassword')
            p.expect('password:')
            p.sendline('dummypasswordagain')
            p.kill(0)
            assert loginpass <> 0, "Failed to login via radius authentication"
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            info(".### Passed SSH login with radius server authentication ###\n")
            return True

    def loginSSHradiusWithLocalPassword(self):
        ''' This is a negative test case to verify login with radius authentication by giving local
        password'''
        info('########## Test to verify SSH login with radius authenication enabled and fallback disabled and using local password ##########\n')
        s1 = self.net.switches [ 0 ]
        # self.checkAccessFiles()
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('admin')
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('admin')
            p.expect('password:')
            p.sendline('admin')
            p.expect('Permission denied')
            p.kill(0)
            info(".### Passed negative test - Authentication fail with local password when radius server authentication enabled ###\n")
            return True
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            assert loginpass <> 1, "Failed to validate radius authetication with local password"

    def loginSSHradiusWithFallback(self):
        ''' This function is to verify radius authentication when fallback is enabled. Login with local
        password should work when raddius server is un reachable'''
        info('########## Test to verify SSH login with radius authenication enabled and fallback Enabled ##########\n')
        s1 = self.net.switches [ 0 ]
        h1 = self.net.hosts [ 0 ]
        h2 = self.net.hosts [ 1 ]
        retFallback = self.FallbackEnable()
        # self.checkAccessFiles()
        host_2_IpAddress = self.getHostIP_2()
        s1.cmdCLI("configure terminal")
        s1.cmdCLI("no radius-server host " + host_2_IpAddress)
        h1.cmd("service freeradius stop")
        h2.cmd("service freeradius stop")

        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('Testing')
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('admin')
            p.expect('#')
            p.sendline('exit')
            p.kill(0)
            s1.cmdCLI("radius-server host " + host_2_IpAddress)
            s1.cmdCLI("exit")
            info(".### Passed authentication with local password when radius server not reachable and fallback enabled ###\n")
            return True
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            s1.cmdCLI("radius-server host " + host_2_IpAddress)
            s1.cmdCLI("exit")
            assert loginpass <> 1, "Failed to validate radius authetication when server is not reachable"

    def loginSSHlocalWrongPassword(self):
        ''' This is a negative test case, we enable only local authetication and try logging with
        wrong password'''
        info('########## Test to verify SSH login with local authenication enabled and Wrong password ##########\n')
        s1 = self.net.switches [ 0 ]
        retFallback = self.noFallbackEnable()
        sleep(5)
        retLocalAuth = self.localAuthEnable()
        sleep(5)
        # self.checkAccessFiles()
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('admin1')
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass=p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('admin2')
            p.expect('password:')
            p.sendline('admin3')
            p.expect('Permission denied')
            p.kill(0)
            info(".### Passed negative test - Authentication fail with wrong local password when local authentication enabled ###\n")
            return True
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            assert loginpass <> 1, "Failed to validate local authentication"

    def loginSSHlocalAgain(self):
        ''' This is again a test case to verify, when local authetication is enabled login should properly
        work with local password'''
        info('########## Test to verify SSH login with local authenication enabled again with correct password ##########\n')
        s1 = self.net.switches [ 0 ]
        # self.checkAccessFiles()
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('admin')
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('admin2')
            p.expect('password:')
            p.sendline('admin3')
            p.expect('Permission denied')
            p.kill(0)
            assert loginpass <> 0, "Failed to validate local authentication with correct password"
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            info(".### Passed authentication with local password when local authentication enabled ###\n")
            return True


    def loginSSHradiusWithSecondaryServer(self):
        '''This function is to verify radius authentication with the secondary radius server
         when unable to reach primary server - radius is true and fallback is false'''
        info('########## Test to verify SSH login with radius authenication enabled and fallback disabled to a secondary radius server ##########\n')
        s1 = self.net.switches [ 0 ]
        retFallback = self.noFallbackEnable()
        sleep(5)
        retAuth = self.radiusAuthEnable()
        sleep(5)
        # self.checkAccessFiles()
        h1 = self.net.hosts [ 0 ]
        h2 = self.net.hosts [ 1 ]
        h1.cmd("service freeradius stop")
        h2.cmd("service freeradius start")
        ssh_newkey = 'Are you sure you want to continue connecting'
        switchIpAddress = self.getSwitchIP()
        myssh = "/usr/bin/ssh admin@" + switchIpAddress
        p = pexpect.spawn(myssh)

        i = p.expect([ssh_newkey, 'password:', pexpect.EOF])

        if i == 0:
            p.sendline('yes')
            i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
        if i == 1:
            p.sendline('testing')
            sleep(2)
        elif i == 2:
            assert i <> 2, "Failed with SSH command"
        loginpass = p.expect(['password:', '#'])
        if loginpass == 0:
            p.sendline('dummypassword')
            p.expect('password:')
            p.sendline('dummypasswordagain')
            p.kill(0)
            assert loginpass <> 0, "Failed to login via secondary radius server authentication"
        if loginpass == 1:
            p.sendline('exit')
            p.kill(0)
            info(".### Passed secondary radius server authentication when primary radius server is not reachable ###\n")
            return True

class Test_aaafeature:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_aaafeature.test = aaaFeatureTest()
        pass

    def teardown_class(cls):
    # Stop the Docker containers, and
    # mininet topology
        Test_aaafeature.test.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test

    def test_setupRadiusserver(self):
        self.test.setupRadiusserver()

    def test_setupRadiusclient(self):
        self.test.setupRadiusclient()

    def test_loginSSHlocal(self):
        self.test.loginSSHlocal()

    def test_loginSSHradius(self):
        self.test.loginSSHradius()

    def test_loginSSHradiusWithLocalPassword(self):
        self.test.loginSSHradiusWithLocalPassword()

    def test_loginSSHradiusWithFallback(self):
        self.test.loginSSHradiusWithFallback()

    def test_loginSSHlocalWrongPassword(self):
        self.test.loginSSHlocalWrongPassword()

    def test_loginSSHlocalAgain(self):
        self.test.loginSSHlocalAgain()

    def test_loginSSHradiusWithSecondaryServer(self):
        self.test.loginSSHradiusWithSecondaryServer()
