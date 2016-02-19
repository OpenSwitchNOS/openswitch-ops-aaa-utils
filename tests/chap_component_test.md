#CHAP Component Test Cases
##Testcases
[TOC]

##Testcase 1: Basic Configuration
*Objective:* Verify if the switch can save the basic configuration of CHAP and PAP.
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
1. Enable PAP Authentication.
2. Save configuration.
3. Check configuration and verify the authentication method.
4. Change to CHAP Authentication.
5. Save configuration.
6. Check configuration and verified the authentication method.

##Testcase 2: Delete Configuration
*Objective:* Verify if the configuration of CHAP and PAP is removed on the Switch.
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
1. Enable PAP Authentication.
2. Save configuration.
3. Check configuration and verified the authentication method.
4. Delete the configuration of switch.
5. Check configuration and verified the authentication method was removed.
6. Enable CHAP Authentication.
7. Save configuration.
8. Check configuration and verified the authentication method.
9. Delete the configuration of CHAP.
10. Check configuration and verified the authentication method was removed.

##Testcase 3: Wrong Configuration
*Objective:* Verify if the switch can allow other options instead of PAP or CHAP.
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
1. Attempt to enable other option using the command.
2. Verify that the switch displays an error message.

##Testcase 4: Save Configuration and Reboot the Switch
*Objective:* Verify if the switch keeps the configuration after reboot.
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
1. Enable PAP Authentication.
2. Save configuration.
3. Check configuration and verified the authentication method.
4. Reboot the Switch.
5. Check configuration and verified the authentication method.
6. Change to CHAP Authentication.
7. Save configuration.
8. Check configuration and verified the authentication method.
9. Reboot the Switch.
10. Check configuration and verified the authentication method.


##Testcase 5: User Authentication
*Objective:* Verify if a user can be authenticated by the Radius Server if CHAP is enable.
*Requirements:*
* Physical or Virtual Switch
* Radius Server

*Setup:*
* Topology Diagram:
         +------------------+          +------------+
         |                  |          |            |
         |  AS5712 switch   |----------|   RADIUS   |
         |                  |          |            |
         +------------------+          +------------+

*Description (Steps):*
1. Configure an IP Address on the Interface of the Radius Server
2. Configure an IP Address on the Interfaces of the Switch
3. Enable the interface of the Switch.
4. Verify connection between all devices
5. Configure RADIUS Server to use CHAP Authentication
6. Add the admin user on the Radius Server.
8. Enable AAA authentication using CHAP Method on swtich.
9. Configure the Radius Server Host on the Switch.
10. Verify the configuration on the Switch.
11. Login to the switch with the admin user.
12. Verify on the logs of the Radius Server that the user was authenticated.


##Testcase 6: User Authentication with wrong configuration
*Objective:* Verify if a user can’t be authenticated with a wrong configuration on the Switch.
*Requirements:*
* Physical or Virtual Switch
* Radius Server

*Setup:*
* Topology Diagram:
         +------------------+          +------------+
         |                  |          |            |
         |  AS5712 switch   |----------|   RADIUS   |
         |                  |          |            |
         +------------------+          +------------+

*Description (Steps):*
1. Configure an IP Address on the Interface of the Radius Server
2. Configure an IP Address on the Interfaces of the Switch
3. Enable the interfaces of the Switch.
4. Verify connection between all devices
5. Configure RADIUS Server to user CHAP Authentication
6. Attempt to login to the switch with the admin user.

##Testcase 7: Admin and netop Authentication
*Objective:* Verify if admin and netop users can be authenticated by the Radius Server if CHAP is enable.
*Requirements:*
* Physical or Virtual Switch
* Radius Server

*Setup:*
* Topology Diagram:
         +------------------+          +------------+
         |                  |          |            |
         |  AS5712 switch   |----------|   RADIUS   |
         |                  |          |            |
         +------------------+          +------------+

*Description (Steps):*
1. Configure an IP Address on the Interface of the Radius Server
2. Configure an IP Address on the Interfaces of the Switch
3. Enable the interfaces of the Switch.
4. Verify connection between all devices
5. Configure RADIUS Server to user CHAP Authentication
6. Add admin and netop users on the Radius Server
7. Enable AAA authentication using CHAP Method.
8. Configure the Radius Server Host on the Switch.
9. Verify the configuration on the Switch.
10. Login to the switch with the admin user.
11. Login to the switch with the netop user.
12. Verify on the logs of the WS that the users were authenticated.

##Testcase 8: Wrong configuration on the Server
*Objective:* Verify if user can’t be authenticated by the Radius Server with wrong configuration.
*Requirements:*
* Physical or Virtual Switch
* Radius Server

*Setup:*
* Topology Diagram:
         +------------------+          +------------+
         |                  |          |            |
         |  AS5712 switch   |----------|   RADIUS   |
         |                  |          |            |
         +------------------+          +------------+
*Description (Steps):*
1. Configure an IP Address on the Interface of the Radius Server 1
2. Configure an IP Address on the Interfaces of the Switch.
3. Enable the interfaces of the Switch.
4. Verify connection between all devices
5. Configure RADIUS Server to use another authentication method instead CHAP
6. Add admin user on the Radius Server
7. Enable AAA authentication using CHAP Method.
8. Configure the Radius Server Host on the Switch.
9. Attempt to authenticate the user through the WS
10. The user can’t be authenticated.

##Testcase 9: Supported Platform
*Objective:* Verify if the CHAP option if only displayed on supported devices.
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
1. Check the platform of the device
2. Verify if the platform supports the CHAP option
3. Attempt to enable AAA authentication using CHAP Method.
4. Verify if the CHAP was enabled or not, according to step 2.
