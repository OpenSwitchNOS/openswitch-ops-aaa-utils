Component Test Cases
============

[toc]

##  Daemon Testing
### Objective
This test is to verify if the daemon is able to get notification of a change in OVSDB and modify the
SSHD Configuration file
### Requirements
The requirements for this test case are:

 - Latest openswitch image with physical Accton AS5712 switch or
 - Latest openswitch VSI image
### Setup
#### Topology Diagram

           AS5712 Switch
         +---------------------------------------------------+
         |                             +---------------+     |
         |                             |               |     |
         |                             |
         |                             |   OVSDB       |     |
         |                             |               |     |
         |                             |               |     |
         | +---------------------+     |               |     |
         | |aaa-utils Daemon     |<----|               |     |
         | +---------------------+     +---------------+     |
         +---------------------------------------------------+
#### Test Setup
### Test case 1.01 : Verify if daemon is running
### Description
Boot the switch with the image and check if aaautilspamcfg daemon is running or not.

### Test Result Criteria
#### Test Pass Criteria
`systemctl status aaautils.service`  should be active and running.
#### Test Fail Criteria
`systemctl status aaautils.service` is suspended or in active.

### Test case 1.02 : Verify if the SSHD configuration file during daemon starts up
### Description
When the daemon starts, verify the SSHD configuration file.

### Test Result Criteria
#### Test Pass Criteria
The SSHD configuration file have the SFTP server disabled.
#### Test Fail Criteria
The SSHD configuration file have the SFTP server enable.

### Test case 1.03 : Verify if the SSHD configuration file is modified to SFTP server enable
### Description
When user enables SFTP server through CLI or REST, SSHD configuration file should be modified accordingly.

### Test Result Criteria
#### Test Pass Criteria
SSHD configuration file modified to enable SFTP server.
#### Test Fail Criteria
SSHD configuration file not modified to enable SFTP server.

### Test case 1.04 : Verify if the SSHD configuration file is modified to SFTP server disable
### Description
When user enables SFTP server through CLI or REST, SSHD configuration file should be modified accordingly.

### Test Result Criteria
#### Test Pass Criteria
SSHD configuration file modified to disnable SFTP server.
#### Test Fail Criteria
SSHD configuration file not modified to disable SFTP server.
