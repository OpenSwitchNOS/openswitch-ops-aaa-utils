#RBAC Component Test Cases
##Testcases
[TOC]

##Testcase 1: Verify admin account
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
4. Verify if the “admin” user is a member of the “ops_admin” group and not a member of “ovsdb_client”.
5. Verify if the user has the appropriate RBAC permissions.

##Testcase 2: Verify netop account
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
3. Verify if the “netop” user is a member of the “ops_netop” and “ovsdb_client” groups
4. Verify if the user has the appropriate RBAC permissions.

##Testcase 3: Configure user with ops\_admin role
*Objective:* Verify if the ops\_admin role can be assigned into a user.
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
3. Verify if the user has the appropriate RBAC permissions.
4. Verify the user has sudo privileges

##Testcase 4: Configure user with ops\_netop role
*Objective:* Verify if the ops\_netop role can be assigned into a user.
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
2. Verify if the user was assigned to the ops\_netop role.
3. Verify if the user has the appropriate RBAC permissions.

##Testcase 5: Configure a user without a role
*Objective:* Verify if the user isn't assigned to a role, it is added to the NO role.
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
1. Create a user and assign it to the NO role on the switch (DUT01)
2. Verify if the user was assigned to the no role.
3. Verify if the user has the appropriate RBAC permissions

##Testcase 6: User assigned to two roles
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
2. Verify if the user was assigned to both roles.
3. Verify the user only has permissions for the admin role.

##Testcase 7: Multiple user, multiple roles
*Objective:* Verify if multiple users can be configured on the switch with their role.
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
1. Create multiple users with their role (Ex. 10 users) on the switch (DUT01)
2. Verify if each user was assigned to the role.

##Testcase 8: Verify RBAC Installation
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
1. Verify rbac.py was installed in the appropriate location.
2. Verify librbac.so and rbac.h were installed in the appropriate locations.

##Testcase 9: Range checking the RBAC interfaces
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
