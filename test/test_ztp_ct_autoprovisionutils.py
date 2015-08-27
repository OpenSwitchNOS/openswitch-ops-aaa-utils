from smart import Error, _
from smart.util import pexpect

import os
import sys
import subprocess
from time import sleep
import pytest

from halonvsi.docker import *
from halonvsi.halon import *

HTTP_SERVER = "http://127.0.0.1/autoprovision"
HTTP_SERVER_ROOT_PATH = "/var/www/servers/www.example.org/pages/"
SCRIPT_NAME = "autoprovision"
TEST_ECHO_STRING = "Hello from Autoprovision script"
LIGHTTPD_CONFIG = "./src/ops-aaa-utils/test/lighttpd.conf"

class autoprovisionFeatureTest(HalonTest):
    def setupHttpServer(self):
        ''' This function is to setup http server in the ubuntu image we are referring to
        '''
        print('\n=========================================================')
        print('*** Setup http server lighttpd ***')
        print('===========================================================')
        s1 = self.net.switches [ 0 ]

        #Configure lighttpd conf file and root path of server
        s1.cmd ("mkdir -p "+ HTTP_SERVER_ROOT_PATH)
        with open(LIGHTTPD_CONFIG) as f_config:
            config = f_config.read()

	s1.cmd(config)
        out = s1.cmd("cat ~/lighttpd.conf")
        out += s1.cmd("echo ")
        print "File Output" + out
        s1.cmd("killall -9 lighttpd")
        sleep(1)
        out = s1.cmd("lighttpd -t -f ~/lighttpd.conf")
        out += s1.cmd("echo ")

        if "Syntax OK" in out:
            print out
        else:
            assert 0, out

        out = s1.cmd("lighttpd -D -f ~/lighttpd.conf &")
        return True

    def setupAutoprovisionScript(self):
        ''' This function is to setup autoprovision script in http server
        '''
        print('\n=========================================================')
        print('*** Setup autoprovision script in http server***')
        print('===========================================================')
        s1 = self.net.switches [ 0 ]
        out = s1.cmd ("touch " + HTTP_SERVER_ROOT_PATH + SCRIPT_NAME)

        s1.cmd ("echo \'#!/bin/sh\' >>" + HTTP_SERVER_ROOT_PATH + SCRIPT_NAME)
        s1.cmd ("echo \'#HALON-AUTOPROVISIONING\'>>" + HTTP_SERVER_ROOT_PATH + SCRIPT_NAME)
        s1.cmd ("echo echo "+TEST_ECHO_STRING+" >>" + HTTP_SERVER_ROOT_PATH + SCRIPT_NAME)
        out = s1.cmd("cat " + HTTP_SERVER_ROOT_PATH + SCRIPT_NAME)
        out += s1.cmd("echo ")
        print out

        return True

    def setupNet(self):
        # Create a topology with single Halon switch
        self.net = Mininet(topo=SingleSwitchTopo(k=1, hopts=self.getHostOpts(), sopts=self.getSwitchOpts()),
                           switch=HalonSwitch,
                           host=HalonHost,
                           link=HalonLink, controller=None,
                           build=True)

        if self.setupHttpServer():
            print 'setupHttpServer success'

        if self.setupAutoprovisionScript():
            print 'setupAutoprovisionScript success'

    def executeAutoprovision(self):
        ''' This function download autoprovision script from http server
        and execute it
        '''
        print('\n=========================================================')
        print('*** Executing Autoprovision ***')
        print('===========================================================')
        s1 = self.net.switches [ 0 ]
        out = s1.cmd("autoprovision "+HTTP_SERVER)
        out += s1.cmdCLI("end")
        print out

        if not TEST_ECHO_STRING in out:
            assert 0,out

        out = s1.cmdCLI("show autoprovision")
        out += s1.cmdCLI("end")
        print out

        if not HTTP_SERVER in out:
            assert 0,out

        print('\n=========================================================')
        print('*** Executing Autoprovision again, it should not perform ***')
        print('===========================================================')
        out = s1.cmd("autoprovision "+HTTP_SERVER)
        out += s1.cmdCLI("end")
        print out

        if not "Autoprovisioning already completed" in out:
            assert 0,out

class Test_autoprovisionfeature:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        Test_autoprovisionfeature.test = autoprovisionFeatureTest()
        pass

    def teardown_class(cls):
    # Stop the Docker containers, and
    # mininet topology
       Test_autoprovisionfeature.test.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test

    def test_executeAutoprovisionself(self):
        if self.test.executeAutoprovision():
            print 'Passed executeAutoprovisionScript'
