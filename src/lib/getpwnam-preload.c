/* Custom implementation of getpwnam functionality.
 *
 * Copyright (C) 2016 Hewlett Packard Enterprise Development LP.
 * This program is free software; you can redistribute it and/or modify it
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
 * along with this program; if not, write to the Free software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 * File: getpwnam-preload.c
 *
 * Purpose: custom implementation of getpwnam function.
 *
 */

#define _GNU_SOURCE
#include <string.h>
#include <sys/types.h>
#include <pwd.h>
#include <dlfcn.h>
#include <syslog.h>
#include <stdio.h>
#include <stdlib.h>

#define xstr(s) str(s)
#define str(s) #s

typedef struct passwd *(*getpwnam_type)(const char *name);
//static const char *last_pw_name = NULL;

struct passwd *getpwnam(const char *name) {
    struct passwd *pw;
    getpwnam_type orig_getpwnam;

    //free((void *) last_pw_name);

    /* TODO: remove the debugs */
    syslog(LOG_ERR, "Tacacs_Dev: entering %s for user %s, TEMPLATE_USER = %s ",
         __FUNCTION__, name, xstr(TEMPLATE_USER));
    orig_getpwnam = (getpwnam_type)dlsym(RTLD_NEXT, "getpwnam");
    pw = orig_getpwnam(name);

    if (pw == NULL) {
        syslog(LOG_ERR, "Tacacs_Dev: (%s) user %s not found locally",
         __FUNCTION__, name);

        /* TODO: rename it to appropriate user */
        pw = orig_getpwnam(xstr(TEMPLATE_USER));
        /*if (pw != NULL) {
            pw->pw_name = strdup(name);
            last_pw_name = pw->pw_name;
        }*/
    }

    return pw;
}
