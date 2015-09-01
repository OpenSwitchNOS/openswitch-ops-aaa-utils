#!/usr/bin/env python
# Copyright (C) 2014-2015 Hewlett-Packard Development Company, L.P.
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

import os
import sys
import urllib2
import httplib
import cookielib
from time import sleep

import ovs.dirs
import ovs.db.idl
from ovs.db import error
from ovs.db import types

# ovs definitions
idl = None
# HALON_TODO: Need to pull this from the build env
DEF_DB = 'unix:/var/run/openvswitch/db.sock'
CFGDB_SCHEMA = '/usr/share/openvswitch/configdb.ovsschema'
OVS_SCHEMA = '/usr/share/openvswitch/vswitch.ovsschema'

# Configuration file definitions
saved_config = None

type_startup_config = "startup"
max_miliseconds_to_wait_for_config_data = 30

OPEN_VSWITCH_TABLE = "Open_vSwitch"
HALON_TRUE = "True"
PERFORMED = "performed"
URL = "url"
AUTOPROVISION_FILE = '/var/tmp/autoprovision'

#------------------ wait_for_config_complete() ----------------
def wait_for_config_complete(idl):

    system_is_configured = 0
    while system_is_configured == 0:
        for ovs_rec in idl.tables[OPEN_VSWITCH_TABLE].rows.itervalues():
            if ovs_rec.cur_cfg is not None and ovs_rec.cur_cfg != 0:
               system_is_configured = ovs_rec.cur_cfg
               break

        poller = ovs.poller.Poller()
        idl.run()
        idl.wait(poller)
        poller.block()

#------------------ check_for_startup_config() ----------------
def check_for_startup_config(remote):
    '''
    Connect to the db server and specify the configdb database.
    Walk through the rows in the config table (if any)
    looking for a row with type == startup.
    '''

    schema_helper_cfg = ovs.db.idl.SchemaHelper(location=CFGDB_SCHEMA)
    schema_helper_cfg.register_table("config")

    idl_cfg = ovs.db.idl.Idl(remote, schema_helper_cfg)

    seqno = idl_cfg.change_seqno  # Sequence number when we last processed the db.

    # Wait until the ovsdb sync up.
    while (seqno == idl_cfg.change_seqno):
        idl_cfg.run()
        poller = ovs.poller.Poller()
        idl_cfg.wait(poller)
        poller.block()

    tbl_found = False

    for ovs_rec in idl_cfg.tables["config"].rows.itervalues():
        if ovs_rec.type:
            if ovs_rec.type == type_startup_config:
                if ovs_rec.config:
					tbl_found = True
                else:
                    print("startup config row does not have config column")
                break

    if not tbl_found:
        print("No startup config rows found in the config table")

    idl_cfg.close()

    return tbl_found

#------------------ fetch_autoprovision_script() ----------------
def fetch_autoprovision_script(url):
    ret = False
    try :
        cj = cookielib.CookieJar()
        header = { 'User-Agent' : 'OPS-AutoProvision/1.0', 'OPS-MANUFACTURER': 'OpenSwitch', 'OPS-VENDOR': 'OpenSwitch' }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = urllib2.Request(url, None, header)

        print("Sending HTTP GET to %s" % url)
        f = opener.open(request)
        data = f.read()
        f.close()
        opener.close()
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
        return ret
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))
        return ret
    except httplib.HTTPException, e:
        print('HTTPException = '+ str(e.reason))
        return ret
    except Exception, e:
        print('generic exception: ' + str(e))
        return ret

    if os.path.exists(AUTOPROVISION_FILE):
        os.remove(AUTOPROVISION_FILE)

    if ("OPS-PROVISIONING" in data):
        FILE = open(AUTOPROVISION_FILE, "wb")
        FILE.write(data)
        FILE.close()
        ret = True
    else :
        print("Error, downloaded autoprovision script doesn't contain OPS-PROVISIONING string in comment")
        ret = False

    return ret

#------------------ update_autoprovision_status() ----------------
def update_autoprovision_status(performed_value, url):
    global idl

    data = {}

    data[PERFORMED] = performed_value
    data[URL] = url
    # create the transaction
    txn = ovs.db.idl.Transaction(idl)
    for ovs_rec in idl.tables[OPEN_VSWITCH_TABLE].rows.itervalues():
        break

    setattr(ovs_rec, "auto_provisioning_status", data)

    txn.commit_block()

    return True


    ###############################  main  ###########################
def main():
    global idl
    argv = sys.argv
    n_args = 2

    if len(argv) !=  n_args :
        print("Requires %d arguments but %d provided \n" % (n_args, len(argv)))
        return

    # Locate default config if it exists
    schema_helper = ovs.db.idl.SchemaHelper(location=OVS_SCHEMA)
    schema_helper.register_columns(OPEN_VSWITCH_TABLE, ["cur_cfg"])
    schema_helper.register_columns(OPEN_VSWITCH_TABLE, ["auto_provisioning_status"])

    idl = ovs.db.idl.Idl(DEF_DB, schema_helper)

    seqno = idl.change_seqno    # Sequence number when we last processed the db

    # Wait until the ovsdb sync up.
    while (seqno == idl.change_seqno):
        idl.run()
        poller = ovs.poller.Poller()
        idl.wait(poller)
        poller.block()

    wait_for_config_complete(idl)

	# HALON_TODO : Need to find a better logic.
    if os.path.exists('/etc/autoprovision'):
        print("Autoprovisioning already completed")
        update_autoprovision_status(HALON_TRUE, argv[1])
        idl.close()
        return

    if(check_for_startup_config(DEF_DB) == True):
        print("startup config present, skipping autoprovision")
        idl.close()
        return

    if(fetch_autoprovision_script(argv[1]) == False):
        print("Downloading autoprovisioning script failed")
        idl.close()
        return

    sys.stdout.flush()

    ret = 1
    if os.path.exists(AUTOPROVISION_FILE):
        ret = os.system('chmod +x ' + AUTOPROVISION_FILE)
        ret = os.system(AUTOPROVISION_FILE)
        if (ret == 0 ):
            update_autoprovision_status(HALON_TRUE, argv[1])
            os.system('touch /etc/autoprovision')
            print("Autoprovision status: performed = %s URL =  %s" % (HALON_TRUE, argv[1]))
        else:
            print("Error, executing autoprovision script returned error %d" % ret)

    idl.close()

if __name__ == '__main__':
    try:
        main()
    except error.Error, e:
        print("Error: \"%s\" \n" % e)
