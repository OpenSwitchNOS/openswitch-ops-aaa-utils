/*
 * Copyright (C) 2016 Hewlett Packard Enterprise Development LP.
 * Copyright (C) 2010, Pawel Krawczyk <pawel.krawczyk@hush.com> and
 * Jeroen Nijhof <jeroen@jeroennijhof.nl>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program - see the file COPYING.
 *
 * File: author_utils.c
 * Purpose: Sends authorization request to the configured server.
 *          Obtains privilege level from the configured server.
 *
 */

#include <stdbool.h>
#include "libtac.h"
#include "openvswitch/vlog.h"

VLOG_DEFINE_THIS_MODULE(author_utils);

/*
 * Wrapper function to receive TACACS authorization parameters from
 * TACC client/CLI and sends authorization request to the configured
 * server.
 * Returns: EXIT_OK    0 when Authorization succeeds.
 *          EXIT_FAIL  1 when Authorization fails.
 *          EXIT_ERR   2 when there is a local error.
 */

int tac_cmd_author(const char *tac_server_name, const char *tac_secret,
                   char *user, char * tty, char *remote_addr,
                   char *service, char *protocol, char *command,
                   int timeout, unsigned char quiet)
{
    int ret;
    int tac_fd;
    int send_status;
    int status_code;
    struct areply arep;
    struct addrinfo *tac_server;
    struct addrinfo hints;
    struct tac_attrib *attr = NULL;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    /* Get addr_info structure for tac_server_name */
    if ((ret = getaddrinfo(tac_server_name, "tacacs", &hints, &tac_server)) != 0) {
        LOG(quiet, ERR, "error: resolving name %s: %s", tac_server_name,
            gai_strerror(ret))
        return EXIT_ERR;
    }

    /* Set TACACS attributes */
    if (command != NULL) {
        tac_add_attrib(&attr, "cmd", command);
    }

    if (protocol != NULL) {
        tac_add_attrib(&attr, "protocol", protocol);
    }

    tac_add_attrib(&attr, "service", service);

    /* TACACS connection to tac_server */
    tac_fd = tac_connect_single(tac_server, tac_secret, NULL, timeout);

    if (tac_fd < 0) {
        LOG(quiet, ERR, "Error connecting to TACACS+ server: %m\n")
        status_code = EXIT_ERR;
        goto CLEAN_UP;
    }

    /* TACACS authorization request to the connected server fd */
    send_status = tac_author_send(tac_fd, user, tty, remote_addr, attr);

    if (send_status < 0) {
        LOG(quiet, ERR, "Authorization request to the server failed\n");
        status_code = EXIT_ERR;
        goto CLEAN_UP;
    }

    /* Read TACACS server authorization response */
    tac_author_read(tac_fd, &arep);

    if (arep.status != AUTHOR_STATUS_PASS_ADD
        && arep.status != AUTHOR_STATUS_PASS_REPL) {
        LOG(quiet, ERR, "Authorization FAILED: %s\n", arep.msg);
        status_code = EXIT_FAIL;
    } else {
        LOG(quiet, INFO, "Authorization OK: %s\n", arep.msg);
        status_code = EXIT_OK;
    }

    CLEAN_UP:
        tac_free_attrib(&attr);
        freeaddrinfo(tac_server);
        return status_code;
}
