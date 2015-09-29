#Autoprovision component test cases
## Contents##
- [Test to verify autoprovision functionality](#test-to-verify-autoprovision-functionality)
- [Test to verify autoprovision executes once](#test-to-verify-autoprovision-executes-once)


## Test cases to verify autoprovision utility ##
### Objective ###
Test cases to verify that autoprovision utility downloads the script from http server and execute it.
### Requirements ###
The requirements for this test case are:

 - AS5712 switch

### Setup ###
#### Topology Diagram ####

			+---------------------------------+
			|                +---------------+|
			|                |Lighttpd server||
			|                | (Http server) ||
			|                +---------------+|
			|                                 |
			|   AS5712 Switch                 |
			|                                 |
			|                                 |
			+---------------------------------+

#### Test Setup ####
Setup a http server and create a hello world shell script in the http servers pages root path.

### Test to verify autoprovision functionality###
#### Description ###
Test to verify whether autoprovision utility downloads the script and executes the downloaded script from URL passed as parameter.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if "show autoprovision" shows autoprovision performed status as yes and URL updated to the OVSDB

#### Test Fail Criteria ####
Testcase result is fail if "show autoprovision" shows autoprovision performed status as no.

### Test to verify autoprovision executes once###
#### Description ###
Test to verify whether autoprovision utility do not execute if autoprovision is already executed. Execute autoprovision utility again in same setup were autoprovision was performed.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if "Autoprovisioning already completed" message is received.

#### Test Fail Criteria ####
Testcase result is fail if "Autoprovisioning already completed" message is not received.
