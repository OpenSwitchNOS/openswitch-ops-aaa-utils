/* AAA CLI commands.
 *
 * Copyright (C) 1997, 98 Kunihiro Ishiguro
 * Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
 *
 * This Program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2, or (at your option) any
 * later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file COPYING.  If not, write to the Free
 * Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 * File: aaa_vty.c
 *
 * Purpose:  To add AAA CLI configuration and display commands.
 */

#include <sys/un.h>
#include <setjmp.h>
#include <sys/wait.h>
#include <pwd.h>

#include <readline/readline.h>
#include <readline/history.h>

#include <lib/version.h>
#include "getopt.h"
#include "vtysh/command.h"
#include "vtysh/memory.h"
#include "vtysh/vtysh.h"
#include "vtysh/vtysh_user.h"
#include "vswitch-idl.h"
#include "ovsdb-idl.h"
#include "aaa_vty.h"
#include "smap.h"
#include "openvswitch/vlog.h"
#include "openswitch-idl.h"
#include "vtysh/vtysh_ovsdb_if.h"
#include "vtysh/vtysh_ovsdb_config.h"
#include <arpa/inet.h>
#include <string.h>

extern struct ovsdb_idl *idl;

static int aaa_show_aaa_authenctication ();
static int show_auto_provisioning ();
static int show_ssh_auth_method ();
static int set_ssh_publickey_auth (const char *status);
static int set_ssh_password_auth (const char *status);

VLOG_DEFINE_THIS_MODULE(vtysh_aaa_cli);

/* Displays AAA Authentication configuration.
 * Shows status of the local authentication [Enabled/Disabled]
 * Shows status of the Radius authentication [Enabled/Disabled]
 * If Radius authentication is enabled, shows Radius authentication
 * type [pap/chap]
 */
static int
aaa_show_aaa_authenctication()
{
    const struct ovsrec_system *row = NULL;

    row = ovsrec_system_first(idl);

    if (!row)
    {
        VLOG_ERR(OVSDB_ROW_FETCH_ERROR);
        return CMD_OVSDB_FAILURE;
    }
    vty_out(vty, "AAA Authentication:%s", VTY_NEWLINE);
    return CMD_SUCCESS;
}

/* CLI to show authentication mechanism configured in DB. */
DEFUN(cli_aaa_show_aaa_authenctication,
        aaa_show_aaa_authenctication_cmd,
        "show aaa authentication",
        SHOW_STR
        "Show authentication options\n" "Show aaa authentication information\n")
{
    return aaa_show_aaa_authenctication();
}

/* Shows auto provisioning status.*/
static int
show_auto_provisioning()
{
    const struct ovsrec_system *row = NULL;

    row = ovsrec_system_first(idl);

    if (!row)
    {
        VLOG_ERR(OVSDB_ROW_FETCH_ERROR);
        return CMD_OVSDB_FAILURE;
    }

    if (smap_get(&row->auto_provisioning_status, "performed") != NULL)
    {
        if (!strcmp
                (smap_get(&row->auto_provisioning_status, "performed"), "True"))
        {
            vty_out(vty, " Performed : %s%s", "Yes", VTY_NEWLINE);
            vty_out(vty, " URL       : %s%s",
                    smap_get(&row->auto_provisioning_status, "url"),
                    VTY_NEWLINE);
        }
        else
        {
            vty_out(vty, " Performed : %s%s", "No", VTY_NEWLINE);
        }
    }

    return CMD_SUCCESS;
}

/* CLI to show auto provisioning status */
DEFUN(cli_show_auto_provisioning,
        show_auto_provisioning_cmd,
        "show autoprovisioning", SHOW_STR "Show auto provisioning status\n")
{
    return show_auto_provisioning();
}

/* Shows ssh authentication method.*/
static int
show_ssh_auth_method()
{
    const struct ovsrec_system *row = NULL;

    row = ovsrec_system_first(idl);

    if (!row)
    {
        VLOG_ERR(OVSDB_ROW_FETCH_ERROR);
        return CMD_OVSDB_FAILURE;
    }

    if (!strcmp
            (smap_get(&row->aaa, SSH_PUBLICKEY_AUTHENTICATION_ENABLE),
                       SSH_AUTH_ENABLE))
    {
        vty_out(vty, " SSH publickey authentication : %s%s", "Enabled",
                VTY_NEWLINE);
    }
    else
    {
        vty_out(vty, " SSH publickey authentication : %s%s", "Disabled",
                VTY_NEWLINE);
    }

    if (!strcmp
            (smap_get(&row->aaa, SSH_PASSWORD_AUTHENTICATION_ENABLE),
                       SSH_AUTH_ENABLE))
    {
        vty_out(vty, " SSH password authentication  : %s%s", "Enabled",
                VTY_NEWLINE);
    }
    else
    {
        vty_out(vty, " SSH password authentication  : %s%s", "Disabled",
                VTY_NEWLINE);
    }

    return CMD_SUCCESS;
}

/* CLI to show authentication mechanism configured in DB */
DEFUN(cli_show_ssh_auth_method,
        show_ssh_auth_method_cmd,
        "show ssh authentication-method",
        SHOW_STR "Show SSH configuration\n" "Show authentication method\n")
{
    return show_ssh_auth_method();
}

/* Set ssh public key aythentication status.*/
static int
set_ssh_publickey_auth(const char *status)
{
    const struct ovsrec_system *row = NULL;
    enum ovsdb_idl_txn_status txn_status;
    struct ovsdb_idl_txn *status_txn = cli_do_config_start();
    struct smap smap_aaa;

    if (status_txn == NULL)
    {
        VLOG_ERR(OVSDB_TXN_CREATE_ERROR);
        cli_do_config_abort(status_txn);
        return CMD_OVSDB_FAILURE;
    }

    row = ovsrec_system_first(idl);

    if (!row)
    {
        VLOG_ERR(OVSDB_ROW_FETCH_ERROR);
        cli_do_config_abort(status_txn);
        return CMD_OVSDB_FAILURE;
    }

    smap_clone(&smap_aaa, &row->aaa);

    if (strcmp(SSH_AUTH_ENABLE, status) == 0)
    {
        smap_replace(&smap_aaa, SSH_PUBLICKEY_AUTHENTICATION_ENABLE,
                      SSH_AUTH_ENABLE);
    }
    else if (strcmp(SSH_AUTH_DISABLE, status) == 0)
    {
        smap_replace(&smap_aaa, SSH_PUBLICKEY_AUTHENTICATION_ENABLE,
                      SSH_AUTH_DISABLE);
    }

    ovsrec_system_set_aaa(row, &smap_aaa);

    txn_status = cli_do_config_finish(status_txn);
    smap_destroy(&smap_aaa);

    if (txn_status == TXN_SUCCESS || txn_status == TXN_UNCHANGED)
    {
        return CMD_SUCCESS;
    }
    else
    {
        VLOG_ERR(OVSDB_TXN_COMMIT_ERROR);
        return CMD_OVSDB_FAILURE;
    }
}

/* CLI to enable ssh public key authentication */
DEFUN(cli_set_ssh_publickey_auth,
        set_ssh_publickey_auth_cmd,
        "ssh public-key-authentication",
        "SSH authentication\n" "Enable publickey authentication method\n")
{
    return set_ssh_publickey_auth(SSH_AUTH_ENABLE);
}

/* CLI to disable ssh public key authentication */
DEFUN(cli_no_set_ssh_publickey_auth,
        no_set_ssh_publickey_auth_cmd,
        "no ssh public-key-authentication",
        NO_STR
        "SSH authentication\n" "Enable publickey authentication method\n")
{
    return set_ssh_publickey_auth(SSH_AUTH_DISABLE);
}

/* Set ssh password authentication.*/
static int
set_ssh_password_auth(const char *status)
{
    const struct ovsrec_system *row = NULL;
    enum ovsdb_idl_txn_status txn_status;
    struct ovsdb_idl_txn *status_txn = cli_do_config_start();
    struct smap smap_aaa;

    if (status_txn == NULL)
    {
        VLOG_ERR(OVSDB_TXN_CREATE_ERROR);
        cli_do_config_abort(status_txn);
        return CMD_OVSDB_FAILURE;
    }

    row = ovsrec_system_first(idl);

    if (!row)
    {
        VLOG_ERR(OVSDB_ROW_FETCH_ERROR);
        cli_do_config_abort(status_txn);
        return CMD_OVSDB_FAILURE;
    }

    smap_clone(&smap_aaa, &row->aaa);

    if (strcmp(SSH_AUTH_ENABLE, status) == 0)
    {
        smap_replace(&smap_aaa, SSH_PASSWORD_AUTHENTICATION_ENABLE,
                      SSH_AUTH_ENABLE);
    }
    else if (strcmp(SSH_AUTH_DISABLE, status) == 0)
    {
        smap_replace(&smap_aaa, SSH_PASSWORD_AUTHENTICATION_ENABLE,
                      SSH_AUTH_DISABLE);
    }

    ovsrec_system_set_aaa(row, &smap_aaa);

    txn_status = cli_do_config_finish(status_txn);
    smap_destroy(&smap_aaa);

    if (txn_status == TXN_SUCCESS || txn_status == TXN_UNCHANGED)
    {
        return CMD_SUCCESS;
    }
    else
    {
        VLOG_ERR(OVSDB_TXN_COMMIT_ERROR);
        return CMD_OVSDB_FAILURE;
    }
}

/* CLI to enable ssh password athentication */
DEFUN(cli_set_ssh_password_auth,
        set_ssh_password_auth_cmd,
        "ssh password-authentication",
        "SSH authentication\n" "Enable password authentication method\n")
{
    return set_ssh_password_auth(SSH_AUTH_ENABLE);
}

/* CLI to disable ssh password athentication */
DEFUN(cli_no_set_ssh_password_auth,
        no_set_ssh_password_auth_cmd,
        "no ssh password-authentication",
        NO_STR "SSH authentication\n" "Enable password authentication method\n")
{
    return set_ssh_password_auth(SSH_AUTH_DISABLE);
}

/*******************************************************************
 * @func        : aaa_ovsdb_init
 * @detail      : Add aaa related table & columns to ops-cli
 *                idl cache
 *******************************************************************/
static void
aaa_ovsdb_init(void)
{
    /* Add AAA columns. */
    ovsdb_idl_add_column(idl, &ovsrec_system_col_aaa);

    /* Add Auto Provision Column. */
    ovsdb_idl_add_column(idl, &ovsrec_system_col_auto_provisioning_status);

    return;
}

/* Initialize AAA related cli node.
 */
void
cli_pre_init(void)
{
    aaa_ovsdb_init();
    return;
}

/* Install  AAA related vty command elements. */
void
cli_post_init(void)
{
    install_element(ENABLE_NODE, &aaa_show_aaa_authenctication_cmd);
    install_element(ENABLE_NODE, &show_auto_provisioning_cmd);
    install_element(ENABLE_NODE, &show_ssh_auth_method_cmd);
    install_element(CONFIG_NODE, &set_ssh_publickey_auth_cmd);
    install_element(CONFIG_NODE, &no_set_ssh_publickey_auth_cmd);
    install_element(CONFIG_NODE, &set_ssh_password_auth_cmd);
    install_element(CONFIG_NODE, &no_set_ssh_password_auth_cmd);

    return;
}
