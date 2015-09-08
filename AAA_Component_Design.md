High level design of OPS-AAA-UTILS
============================

aaa-utils core component is aaa-utils daemon. The primary goal of this daemon is to modify pam configuration files, ssh configuration file and radius client file accordingly by the values saved in OVSDB. The OVSDB values are configured using CLI.

Responsibilities
---------------
The aaa-utils daemon has a ability to listen to the changes in OVSDB. When the daemon gets a notification of change in the OVSDB, it goes and modify respective files.

Design choices
--------------
The daemon is written in python, as the main aim of daemon is to modify configuration files.

	    +------------------------+
	    | OVSDB - aaa            |
	    |       - Radius Server  |
	    +----^-------------------+
	         |
	         |                        +----------------------------------+
	         |                        |                                  |
	         +              +-------->|       Radius client              |
	         |              |         |                                  |
	         |              |         +----------------------------------+
	         |              |
	         |              |         +----------------------------------+
	         |              |         |                                  |
	    +----v----------+   +-------->|    SSH configuration file        |
	    |               |   |         |                                  |
	    |   DAEMON      |   |         +----------------------------------+
	    |  aaa-utils    +---+
	    |               |   |         +----------------------------------+
	    |               |   |         |                                  |
	    +---------------+   +-------->|     PAM configuration files      |
	                                  |                                  |
	                                  +----------------------------------+

References
----------
* [Reference 1](http://www.openswitch.net/docs/redest1)
* ...

TBD: Include references CLI, REST.
