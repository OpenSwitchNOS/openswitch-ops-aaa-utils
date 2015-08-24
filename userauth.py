#!/usr/bin/env python
# Copyright (C) 2015 Hewlett-Packard Development Company, L.P.
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

import tornado.web
import PAM

val = ''

def is_user_authenticated(param):
    if not param.get_secure_cookie("user"):
        return False
    else:
        return True

def pam_conv(auth, query_list, userData):
    global val
    resp = []
    resp.append((val, 0))
    return resp

def handle_user_login(param):
    global val

    service = 'rest'
    auth = PAM.pam()
    auth.start(service)
    user = param.get_argument("name")
    val = param.get_argument("password")
    auth.set_item(PAM.PAM_USER, user)
    auth.set_item(PAM.PAM_CONV, pam_conv)
    return auth.authenticate()
