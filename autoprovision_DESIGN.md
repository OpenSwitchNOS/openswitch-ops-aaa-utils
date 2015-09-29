# High level design of autoprovisioning
[toc]

## Feature description
Autoprovisioning is implemented by adding hooks to DHCP client. Openswitch uses dhclient package which allows the users to add entry and exit hooks. A new exit hook is added to process the DHCP options.

## Responsibilities
* Process incoming DHCP replies and extract option 239
* Execute autoprovisioning procedure and update the status in OVSDB

## Design choices
The design choice was to avoid making any code changes to dhclient and extend the functionality by mechanisms supported by dhclient.

## Relationships to external OpenSwitch entities
It interacts with OVSDB and DHClient package.

## OVSDB-Schema
Column **auto\_provisioning_status** present in System table is used to store the status of autoprovision.

## Internal structure
It is implemented using python. The file autoprovision.py is called by dhclient exit hook passing the value of option 239 (URL of provisioning script on server) as argument. The code performs following actions:

- Connects to OVSDB and builds the idl object
- Fetches the provisioning script from the specified URL
- Executes the script
- Updates the autoprovision status to the OVSDB table System, column auto_provisioning_status.

## References
For Command Reference document of autoprovision, refer to [Autoprovision Command Reference - TBL](autoprovision_CLI.md)
