/* priv_level.c: Get privilege level of the user from the server.
 *
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
 * Author: Nilesh Shinde <nilesh.shinde@hpe.com>
 */

#include "libtac.h"

/* This function sets privilege level of the user for "PRIV_LVL" env ariable*/

void get_priv_level(struct addrinfo *tac_server, char *tac_secret,
			char *user, char *tty, char *remote_addr,
                        unsigned char quiet) {

	struct tac_attrib *attr = NULL;
	tac_add_attrib(&attr, "service", "shell");
        tac_add_attrib(&attr, "cmd", "");
        struct tac_attrib *ret_attr = NULL;
        char *ret_sep = NULL;
        int tac_fd;
        struct areply arep;
	char *set_attribute = "PRIV_LVL";

        tac_fd = tac_connect_single(tac_server, tac_secret, NULL, 60);
	if (tac_fd < 0) {
		if (!quiet)
			printf("Error connecting to TACACS+ server: %m\n");
		exit(2);
	}

	tac_author_send(tac_fd, user, tty, remote_addr, attr);

	tac_author_read(tac_fd, &arep);

        ret_attr = arep.attr;
        char attr_ret[ret_attr->attr_len];
	char value[ret_attr->attr_len];
	ret_sep = index(ret_attr->attr, '=');
	if (ret_sep != NULL) {
		strncpy(attr_ret, ret_attr->attr, ret_attr->attr_len - strlen(ret_sep));
		attr_ret[ret_attr->attr_len - strlen(ret_sep)] = '\0';
		strncpy(value, ret_sep+1, strlen(value));
		value[strlen(ret_sep)+1] = '\0';
		setenv(set_attribute, value, 1);
                /* To make sure that the privilege level env is set and returned*/
                printf("Returned privilege level for user %s : %s\n",
                        user, getenv(set_attribute));
	}

	if (arep.status != AUTHOR_STATUS_PASS_ADD
			&& arep.status != AUTHOR_STATUS_PASS_REPL) {
		if (!quiet)
			printf("Authorization FAILED: %s\n", arep.msg);
		exit(1);
	} else {
		if (!quiet)
			printf("Authorization OK: %s\n", arep.msg);
	}

	tac_free_attrib(&attr);
        tac_free_attrib(&ret_attr);
}
