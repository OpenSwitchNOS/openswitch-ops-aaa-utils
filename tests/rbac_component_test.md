#RBAC Component Test Cases
##Testcases
[TOC]
##Testcase 1: Verify root account
*Objective:* Verify if the "root" account was created properly in the system.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
*Topology Diagram:
             +------------------+
             |                  |
             |  AS5712 switch   |
             |                  |
             +------------------+

*Description (Steps):*
1. Verify the user “root” and the password was created on the system (DUT01)
2. Verify the “root” user started in the bash shell
3. Verify if the user has system management permissions(SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).

##Testcase 2: Verify admin account
*Objective:* Verify that the “admin” account was created properly in the system.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Verify the user “admin” and the password was created on the system (DUT01)
2. Verify the “admin” user started in the bash shell
3. Verify the “admin” user has sudo privileges
4. Verify if the “admin” user is a member of the “ops_admin” group and not a member of “ovsdb-client”.
5. Verify if the user has system management permissions(SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).

##Testcase 3: Verify netop account
*Objective:* Verify that the “netop” account was created properly in the system.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Verify the user “netop” and the password was created on the system (DUT01)
2. Verify the “netop” user started in the vtysh shell
3. Verify if the “netop” user is a member of the “ops_netop” and “ovsdb-client” groups
4. Verify if the user only has newtork operator permissions.(READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG)
5. Verify the netop user does not have sudo permissions.
6. Verify the netop user does not have system management permission(SYS_MGMT)

##Testcase 4: Configure a new user with ops\_admin role
*Objective:* Verify if a new user can be assigned to the ops\_admin role.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Create a user and assign it to the ops\_admin role on the switch (DUT01)
2. Verify if the user was assigned to ops\_admin role.
3. Verify if the user started in the bash shell
4. Verify if the user has sudo privileges
5. Verify if the user has system management permissions(SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).

##Testcase 5: Configure user with ops\_netop role
*Objective:* Verify if a new user can be assigned to the ops_netop role.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Create a user and assign it to the ops\_netop role on the switch (DUT01)
2. Verify the  user started in the vtysh shell
3. Verify if the user is a member of the “ops_netop” and “ovsdb-client” groups
4. Verify if the user only has network operator permissions.(READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG)
5. Verify the user does not have sudo permissions.
6. Verify the user does not have system management permission (SYS_MGMT)


##Testcase 6: Configure a user without a role
*Objective:* Verify if a no role user has no permissions.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Create a user without a role  on the switch (DUT01)
2. Verify if the user does not belong to admin or netop role.
3. Verify if the user does not have system management permissions(SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).

##Testcase 7: Non-existent user
*Objective:* Verify if a non-existent user does not have permissions.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
 * Topology Diagram:
               +------------------+
               |                  |
               |  AS5712 switch   |
               |                  |
               +------------------+

*Description (Steps):*
1. Verify if a non-existent user does not belong to admin or netop role.
2. Verify if the user does not have system management permissions(SYS_MGMT).
3. Verify if the user does not have network operator permissions(READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).


##Testcase 8: User assigned to two roles
*Objective:* Verify permission of a user assigned to multiple roles.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Create a user and assign it to the ops\_netop and ops\_admin role on the switch (DUT01)
2. Verify if the user was assigned only to ops\_admin role.
3. Verify if the user started in the bash shell
4. Verify if the user has sudo privileges
5. Verify if the user has system management permissions(SYS_MGMT, READ_SWITCH_CONFIG, WRITE_SWITCH_CONFIG).

##Testcase 9: Verify RBAC Installation
*Objective:* Verify that the RBAC files (python and librbac.so) where installed in the appropriate locations.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Verify rbac.py was installed in the appropriate location (/usr/lib/python2.7/site-packages/).
2. Verify librbac.so and rbac.h were installed in the appropriate locations(/usr/include).

##Testcase 10: Range checking the RBAC interfaces
*Objective:* Verify the RBAC interfaces return the appropriate results when passed bad data.
*Requirements:*
* Physical or Virtual Switch

*Setup:*
* Topology Diagram:
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

*Description (Steps):*
1. Pass in a non-existent user name into the RBAC API’s
2. Pass in a null user name into the RBAC API’s where applicable
3. Pass in a null rbac_permission_t pointer into RBAC API’s where applicable
4. Pass in a null rbac_role_t pointer into RBAC API’s where applicable.
