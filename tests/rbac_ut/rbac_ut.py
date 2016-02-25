#!/usr/bin/env python
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# =======================================================
# Module: rbac_ut.py
# Description: Unit Test for RBAC interface
# =======================================================
import rbac
import time
import subprocess
import os

#
# Used to create user accounts
#
GROUP_OPS_ADMIN = "ops_admin"
GROUP_OPS_NETOP = "ops_netop"
GROUP_NONE = "users"

#
# Roles
#
ROLE_ROOT = "root"
ROLE_ADMIN = "ops_admin"
ROLE_NETOP = "ops_netop"
ROLE_NONE = "none"
ROLE_EMPTY = ""

#
# Users
#
USER_ROOT = "root"
USER_ADMIN_BI = "admin"
USER_NETOP_BI = "netop"
USER_ADMIN = "rbactest_admin"
USER_NETOP = "rbactest_netop"
USER_GENERIC = "rbactest_generic"
USER_BOTH = "rbactest_both"
USER_BOGUS = "I_DONT_EXIST"
USER_BLANK = ""
USER_NETOP_SHORT = "neto"
USER_NETOP_LONG = "netopp"
USER_ADMIN_SHORT = "adm"
USER_ADMIN_LONG = "adminn"

#
# Supported Permissions
#
READ_SWITCH_CONFIG = "READ_SWITCH_CONFIG"
WRITE_SWITCH_CONFIG = "WRITE_SWITCH_CONFIG"
SYS_MGMT = "SYS_MGMT"

#
# Supported Permissions for each role
#
ROLE_ROOT_PERMISSIONS = [SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG]
ROLE_ADMIN_PERMISSIONS = [SYS_MGMT]
ROLE_NETOP_PERMISSIONS = [READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG]
ROLE_NONE_PERMISSIONS = []
NO_USER_PERMISSIONS = []

#
# Global test variables
#
passed_tests = 0
failed_tests = 0


#
# These four function do a bulk of the work calling the rbac interfaces
# and making sure we receive the expected results. The expected results
# are passed in from the individual test cases.
#
# The print statements in these routines have been commented out and
# my be useful to un-comment when tracking down failing tests.
#
# Returning a 0 is a passing test case
# Returning a 1 is a failing test case
#
def rbac_ut_rbac_get_user_role(username, role):

    # print "---Checking role ", username
    rbacrole = rbac.get_user_role(username)
    if role not in rbacrole:
        # print "role is", role
        # print "rbacrole is", rbacrole
        # print "===Checking user role - failed"
        return(1)
    # print "   Checking user role - passed"
    return(0)


def rbac_ut_rbac_check_user_permission(username, permission, expected_result):
    # print "---Checking user permission", permission, "for user",\
    # username, "for result", expected_result
    rbacresult = rbac.check_user_permission(username, permission)
    if rbacresult != expected_result:
        # print "===Checking user permission - failed"
        return(1)
    # print "   Checking user permission - passed"
    return(0)


def rbac_ut_rbac_get_user_permissions(username, permissionlist):
    # print "---Getting user permissions for user", username
    rbacpermissions = rbac.get_user_permissions(username)
    if len(permissionlist) != len(rbacpermissions):
        # print "permissionlist len", len(permissionlist)
        # print "rbacpermissions", len(rbacpermissions)
        # print "===Getting user permission - failed (lists different size)"
        return(1)
    permissionlist.sort()
    rbacpermissions.sort()
    result = cmp(permissionlist, rbacpermissions)
    if result == 0:
        # print "   Getting user permission - passed"
        return(0)
    # print "permissionlist", permissionlist
    # print "rbacpermissions", rbacpermissions
    # print "===Getting user permission - failed (lists have different values)"
    return(1)


#
# Creates the user accounts used in both python and C unit tests
#
def create_user_accounts():
    print "---Creating user account ", USER_ADMIN
    cmd = []
    cmd.insert(0, "/usr/sbin/useradd")
    cmd.insert(1, "-g")
    cmd.insert(2, GROUP_OPS_ADMIN)
    cmd.insert(3, "-s")
    cmd.insert(4, "/sbin/bash")
    cmd.insert(5, USER_ADMIN)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Creating user account ", USER_NETOP
    cmd.remove(USER_ADMIN)
    cmd = []
    cmd.insert(0, "/usr/sbin/useradd")
    cmd.insert(1, "-g")
    cmd.insert(2, GROUP_OPS_NETOP)
    cmd.insert(3, "-G")
    cmd.insert(4, "ovsdb-client")
    cmd.insert(5, "-s")
    cmd.insert(6, "/usr/bin/vtysh")
    cmd.insert(7, USER_NETOP)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Creating user account ", USER_GENERIC
    cmd = []
    cmd.insert(0, "/usr/sbin/useradd")
    cmd.insert(1, "-g")
    cmd.insert(2, GROUP_NONE)
    cmd.insert(3, "-s")
    cmd.insert(4, "/sbin/bash")
    cmd.insert(5, USER_GENERIC)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Creating user account ", USER_BOTH
    cmd = []
    cmd.insert(0, "/usr/sbin/useradd")
    cmd.insert(1, "-g")
    cmd.insert(2, GROUP_OPS_NETOP)
    cmd.insert(3, "-G")
    cmd.insert(4, GROUP_OPS_ADMIN + ",ovsdb-client")
    cmd.insert(5, "-s")
    cmd.insert(6, "/sbin/bash")
    cmd.insert(7, USER_BOTH)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)


#
# Deletes the user accounts that were used in both python and C testing
#
def delete_user_accounts():
    print "---Deleting user account ", USER_ADMIN
    cmd = []
    cmd.insert(0, "/usr/sbin/userdel")
    cmd.insert(1, "-r")
    cmd.insert(2, USER_ADMIN)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Deleting user account ", USER_NETOP
    cmd = []
    cmd.insert(0, "/usr/sbin/userdel")
    cmd.insert(1, "-r")
    cmd.insert(2, USER_NETOP)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Deleting user account ", USER_GENERIC
    cmd = []
    cmd.insert(0, "/usr/sbin/userdel")
    cmd.insert(1, "-r")
    cmd.insert(2, USER_GENERIC)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

    print "---Deleting user account ", USER_BOTH
    cmd = []
    cmd.insert(0, "/usr/sbin/userdel")
    cmd.insert(1, "-r")
    cmd.insert(2, USER_BOTH)
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    time.sleep(5)

#
# These are the individual test cases. I have tried to structure then
# so they closely match the unittest test cases for the "C" shared library.
#


#
# Test the rbac.get_user_role() interface
#
def rbac_get_user_role_multiple_users():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_role_multiple_users"

    tf = 0
    tf += rbac_ut_rbac_get_user_role(USER_ROOT, ROLE_ROOT)
    tf += rbac_ut_rbac_get_user_role(USER_ADMIN_BI, ROLE_ADMIN)
    tf += rbac_ut_rbac_get_user_role(USER_NETOP_BI, ROLE_NETOP)
    tf += rbac_ut_rbac_get_user_role(USER_ADMIN, ROLE_ADMIN)
    tf += rbac_ut_rbac_get_user_role(USER_NETOP, ROLE_NETOP)
    tf += rbac_ut_rbac_get_user_role(USER_GENERIC, ROLE_NONE)
    tf += rbac_ut_rbac_get_user_role(USER_BOGUS, ROLE_EMPTY)
    tf += rbac_ut_rbac_get_user_role(USER_BLANK, ROLE_EMPTY)
    tf += rbac_ut_rbac_get_user_role(USER_BOTH, ROLE_ADMIN)
    tf += rbac_ut_rbac_get_user_role(USER_ADMIN_SHORT, ROLE_EMPTY)
    tf += rbac_ut_rbac_get_user_role(USER_ADMIN_LONG, ROLE_EMPTY)
    tf += rbac_ut_rbac_get_user_role(USER_NETOP_SHORT, ROLE_EMPTY)
    tf += rbac_ut_rbac_get_user_role(USER_NETOP_LONG, ROLE_EMPTY)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_role_multiple_users"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_role_multiple_users"


#
# Tests the rbac.check_user_permission() interface
# with built-in root user
#
def rbac_check_user_permission_root():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_root"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, rbac.READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, rbac.WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, rbac.SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ROOT, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_root"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_root"


#
# Tests the rbac.check_user_permission() interface
# with built-in admin user
#
def rbac_check_user_permission_builtin_admin():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_builtin_admin"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, rbac.SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_BI, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_builtin_admin"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_builtin_admin"


#
# Tests the rbac.check_user_permission() interface
# with built-in netop user
#
def rbac_check_user_permission_builtin_netop():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_builtin_netop"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, rbac.READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, rbac.WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, rbac.SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_BI, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_builtin_netop"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_builtin_netop"


#
# Tests the rbac.check_user_permission() interface
# with created user with ops_admin
#
def rbac_check_user_permission_user_ops_admin():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_ops_admin"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, rbac.SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_ops_admin"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_ops_admin"


#
# Tests the rbac.check_user_permission() interface
# with created user with ops_netop
#
def rbac_check_user_permission_user_ops_netop():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_ops_netop"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, rbac.READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, rbac.WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, rbac.SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, READ_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, WRITE_SWITCH_CONFIG, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_ops_netop"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_ops_netop"


#
# Tests the rbac.check_user_permission() interface
# with created user with no ops role
#
def rbac_check_user_permission_user_generic():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_generic"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, rbac.SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_GENERIC, "KJDSFKJDSK", False)

    global failed_tests
    global passed_tests

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_generic"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_generic"


#
# Tests the rbac.check_user_permission() interface
# with unknown user
#
def rbac_check_user_permission_user_bogus():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_bogus"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, rbac.SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOGUS, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_bogus"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_bogus"


#
# Tests the rbac.check_user_permission() interface
# with blank user name
#
def rbac_check_user_permission_user_blank():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_blank"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, rbac.SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, SYS_MGMT, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BLANK, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_blank"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_blank"


#
# Tests the rbac.check_user_permission() interface
# with a user with both ops_admin and ops_netop role
#
def rbac_check_user_permission_user_multiple_roles():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_user_multiple_roles"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, rbac.SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, SYS_MGMT, True)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, "", False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_BOTH, "KJDSFKJDSK", False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_user_multiple_roles"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_user_multiple_roles"


#
# Tests the rbac.check_user_permission() interface
# with a partial valid user name
#
def rbac_check_user_permission_partial_user_names():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_check_user_permission_partial_user_name"

    tf = 0
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_SHORT, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_SHORT, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_SHORT, rbac.SYS_MGMT, False)

    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_LONG, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_LONG, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_ADMIN_LONG, rbac.SYS_MGMT, False)

    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_SHORT, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_SHORT, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_SHORT, rbac.SYS_MGMT, False)

    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_LONG, rbac.READ_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_LONG, rbac.WRITE_SWITCH_CONFIG, False)
    tf += rbac_ut_rbac_check_user_permission(
                       USER_NETOP_LONG, rbac.SYS_MGMT, False)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_check_user_permission_partial_user_names"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_check_user_permission_partial_user_name"


#
# Tests the rbac.get_user_permissions() interface
# with built-in root user.
#
def rbac_get_user_permissions_user_root():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_root"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ROOT, rbac.ROLE_ROOT_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ROOT, ROLE_ROOT_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_root"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_root"


#
# Tests the rbac.get_user_permissions() interface
# with built-in admin user.
#
def rbac_get_user_permissions_user_builtin_admin():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_builtin_admin"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN_BI, rbac.ROLE_ADMIN_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN_BI, ROLE_ADMIN_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_builtin_admin"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_builtin_admin"


#
# Tests the rbac.get_user_permissions() interface
# with built-in netop user.
#
def rbac_get_user_permissions_user_builtin_netop():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_builtin_netop"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP_BI, rbac.ROLE_NETOP_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP_BI, ROLE_NETOP_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_builtin_netop"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_builtin_netop"


#
# Tests the rbac.get_user_permissions() interface
# using a created user with ops_admin role
#
def rbac_get_user_permissions_user_ops_admin():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_ops_admin"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN, rbac.ROLE_ADMIN_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN, ROLE_ADMIN_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_ops_admin"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_ops_admin"


#
# Tests the rbac.get_user_permissions() interface
# using a created user with ops_netop role
#
def rbac_get_user_permissions_user_ops_netop():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_ops_netop"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP, rbac.ROLE_NETOP_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP, ROLE_NETOP_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_ops_netop"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_ops_netop"


#
# Tests the rbac.get_user_permissions() interface
# using a created user with no ops role
#
def rbac_get_user_permissions_user_generic():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_generic"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_GENERIC, rbac.ROLE_NONE_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_GENERIC, ROLE_NONE_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_generic"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user generic"


#
# Tests the rbac.get_user_permissions() interface
# using a bogus user name
#
def rbac_get_user_permissions_user_bogus():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_bogus"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(USER_BOGUS, NO_USER_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_bogus"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user bogus"


#
# Tests the rbac.get_user_permissions() interface
# using a blank user name
#
def rbac_get_user_permissions_user_blank():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_blank"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(USER_BLANK, NO_USER_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_blank"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_blank"


#
# Tests the rbac.get_user_permissions() interface
# using a created user with both ops_admin and ops_netop role
#
def rbac_get_user_permissions_user_multiple_roles():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_user_multiple_roles"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_BOTH, rbac.ROLE_ADMIN_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_BOTH, ROLE_ADMIN_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_user_multiple_roles"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_user_mulitple_roles "


#
# Tests the rbac.get_user_permissions() interface
# using a partial built-in user name
#
def rbac_get_user_permissions_partial_user_names():

    global failed_tests
    global passed_tests

    print "[ RUN      ]  rbac_get_user_permissions_partial_user_names"

    tf = 0
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN_SHORT, NO_USER_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_ADMIN_LONG, NO_USER_PERMISSIONS)

    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP_SHORT, NO_USER_PERMISSIONS)
    tf += rbac_ut_rbac_get_user_permissions(
                       USER_NETOP_LONG, NO_USER_PERMISSIONS)

    if tf > 0:
        failed_tests += 1
        print "Value of:  ", tf
        print "Expected:  0"
        print "[  FAILED  ]  rbac_get_user_permissions_parital_user_names"
    else:
        passed_tests += 1
        print "[      OK  ]  rbac_get_user_permissions_partial_user_names"


#
# This is the main function that will run all the RBAC Python unit tests.
#
def rbac_ut():
    #
    #   Setup
    #

    # print "Creating user accounts"
    # create_user_accounts()

    print ""
    print ""
    print "rbac_ut Test Harness for python libraries"
    print "[==========]"
    print "[----------]"

#
# Run the python unit tests
#
    print "[----------]"
    print "Running rbac.check_user_permissions() tests"

    #
    # get_user_role tests
    #
    rbac_get_user_role_multiple_users()

    #
    # check user permission tests
    #
    rbac_check_user_permission_root()
    rbac_check_user_permission_builtin_admin()
    rbac_check_user_permission_builtin_netop()
    rbac_check_user_permission_user_ops_admin()
    rbac_check_user_permission_user_ops_netop()
    rbac_check_user_permission_user_generic()
    rbac_check_user_permission_user_bogus()
    rbac_check_user_permission_user_blank()
    rbac_check_user_permission_user_multiple_roles()
    rbac_check_user_permission_partial_user_names()

    #
    # get user permissions tests
    #
    rbac_get_user_permissions_user_root()
    rbac_get_user_permissions_user_builtin_admin()
    rbac_get_user_permissions_user_builtin_netop()
    rbac_get_user_permissions_user_ops_admin()
    rbac_get_user_permissions_user_ops_netop()
    rbac_get_user_permissions_user_generic()
    rbac_get_user_permissions_user_bogus()
    rbac_get_user_permissions_user_blank()
    rbac_get_user_permissions_user_multiple_roles()
    rbac_get_user_permissions_partial_user_names()

    #
    # Results
    #
    print "[----------] ", passed_tests + failed_tests, "from rbac_ut"
    print ""
    print "[==========] ", passed_tests + failed_tests, "from rbac_ut"
    if passed_tests > 0:
        print "[  PASSED  ] ", passed_tests
    if failed_tests > 0:
        print "[  FAILED  ] ", failed_tests
    print ""
    print ""

    #
    # Teardown
    #

    # print "Deleting user accounts"
    # delete_user_accounts()

    return(0)
