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
# =======================================================
# Module: cookiesecret.py
# Description: functions to manage cookie secret value
# =======================================================

import OpenSSL
import os

# =======================================================
# Function: generate_cookie_secret.py
# Description: generate value to be used as cookie secret
#              By default set_secure_cookie uses HMAC-SHA-
#              256.Using 44 bytes(>256 bits)as cookie
#              secret length.
# =======================================================

def generate_cookie_secret():
   if os.path.isfile('/var/run/persistant_cookie_secret'):
       with open('/var/run/persistant_cookie_secret','r') as file:
           string2 = file.read()
   else:
       string1 = os.urandom(44)
       OpenSSL.rand.seed(string1)
       string2 = OpenSSL.rand.bytes(44)
       file = open('/var/run/persistant_cookie_secret', 'w+')
       file.write(string2)
       file.close()
       os.chmod("/var/run/persistant_cookie_secret",0600)
   return string2
