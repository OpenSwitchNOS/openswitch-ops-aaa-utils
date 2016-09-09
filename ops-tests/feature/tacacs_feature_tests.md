# TACACS+ Authentication Feature Test Cases

## Contents

- [Test local authentication](#test-local-authentication)
- [Test TACACS+ authentication](#test-tacacs-authentication)
- [Test TACACS+ authentication with fail-through](#test-tacacs-authentication-with-fail-through)
- [Test local authentication with fail-through](#test-local-authentication-with-fail-through)

## Test local authentication

### Objective
This test case validates if user able to login to switch with local authentication enabled
or no aaa authentication configured (local authentication enabled by default)

### Requirements
- Docker: up-to-date OpenSwitch docker image and pre-configured openswitch/tacacs_server image
- Physical: AS5712 switch loded with up-to-date OpenSwitch image, two TACACS+ servers


### Setup

#### Topology diagram
```ditaa
+----------+   +----------+   +----------+
|  Host 1  +---+  Switch  +---+  Host 1  |
+----------+   +----------+   +----------+
```
#### Test Setup

##### TACACS+ server setup
Restart TACACS+ service on two hosts
```
service tac_plus stop
service tac_plus start
```

##### Authentication client (OpenSwitch) setup
1. Add user netop (password: netop) to swith
2. Configure the switch as Authentication client
```
configure terminal
aaa authentication login default local
```
3. Remove aaa authentication configuration and local authentication should still pass
```
configure terminal
no aaa authentication login default
```

### Test result criteria

#### Test pass criteria
Local user netop (password: netop) able to pass local authentication and login to OpenSwitch

#### Test Fail Criteria
Local user netop failed to login after provide password three times



## Test TACACS+ authentication

### Objective
This test case validates if user able to login to switch with TACACS+ server authentication enabled


### Requirements
- Docker: up-to-date OpenSwitch docker image and pre-configured openswitch/tacacs_server image
- Physical: AS5712 switch loded with up-to-date OpenSwitch image, two TACACS+ servers


### Setup

#### Topology diagram
```ditaa
+----------+   +----------+   +----------+
|  Host 1  +---+  Switch  +---+  Host 2  |
+----------+   +----------+   +----------+
```
#### Test Setup

##### TACACS+ server setup
1. Disable TACACS+ service on two hosts
```
service tac_plus stop
```
2. Configure passkey(authentication key) on both host, passkey should show up in
   **/etc/tacacs/tac_plus.conf** as following:
```
key = "tac_test"
```
3. Create user user1 on host 1, user1 should show up in **/etc/tacacs/tac_plus.conf** as following:
```
  user = user1 {
        pap = cleartext user1
        service = exec {
         priv-lvl = 14
        }
  }
```
4. Enable TACACS+ service on two hosts
```
service tac_plus start
```

##### Authentication client (OpenSwitch) setup
1. Get ip address of two hosts
2. Configure the switch as TACACS+ authentication client and add two TACACS+ hosts
```
configure terminal
tacacs-server host 172.17.0.2 key tac_test
tacacs-server host 172.17.0.3 key tac_test
aaa group server tacacs+ sg1
(config-sg) server 172.17.0.2
exit
aaa group server tacacs+ sg2
(config-sg) server 172.17.0.3
exit
aaa authentication login default group sg1 sg2
```


### Description
User should be able to pass TACACS+ server authentication and login to switch use
username/password configured on primary TACACS+ server


### Test result criteria

#### Test pass criteria
User user1 (password: user1) able to pass TACACS+ server authentication and login to OpenSwitch

#### Test Fail Criteria
User user1 failed to login after provide password three times



## Test TACACS+ authentication with fail-through

### Objective
This test case validates if user able to login to switch with TACACS+ server authentication and
fail-through enabled.


### Requirements
- Docker: up-to-date OpenSwitch docker image and pre-configured openswitch/tacacs_server image
- Physical: AS5712 switch loded with up-to-date OpenSwitch image, two TACACS+ servers


### Setup

#### Topology diagram
```ditaa
+----------+   +----------+   +----------+
|  Host 1  +---+  Switch  +---+  Host 2  |
+----------+   +----------+   +----------+
```
#### Test Setup

##### TACACS+ server setup
1. Disable TACACS+ service on two hosts
```
service tac_plus stop
```
2. Configure passkey(authentication key) on both host, passkey should show up in
   **/etc/tacacs/tac_plus.conf** as following:
```
key = "tac_test"
```
3. Create user mario on host 2, mario should show up in **/etc/tacacs/tac_plus.conf** as following:
```
  user = mario {
        pap = cleartext super
        service = exec {
         priv-lvl = 15
        }
  }
```
4. Enable TACACS+ service on two hosts
```
service tac_plus start
```

##### Authentication client (OpenSwitch) setup
1. Get ip address of two hosts
2. Configure the switch as TACACS+ authentication client and add two TACACS+ hosts
```
configure terminal
tacacs-server host 172.17.0.2 key tac_test
tacacs-server host 172.17.0.3 key tac_test
aaa group server tacacs+ sg1
(config-sg) server 172.17.0.2
exit
aaa group server tacacs+ sg2
(config-sg) server 172.17.0.3
exit
aaa authentication login default group sg1 sg2
aaa authentication allow-fail-through
```
3. After verified TACACS+ authentication success, disable fail-through option and
   verify TACACS+ authentication fail
```
configure terminal
no aaa authentication allow-fail-through
```


### Description
User should be able to pass TACACS+ server authentication and login to switch use
username/password configured on secondary TACACS+ server with fail-through enabled


### Test result criteria

#### Test pass criteria
1. User mario (password: super) able to pass TACACS+ server authentication and login to OpenSwitch
   with allow-fail-through enabled
2. User mario (password: super) not able to pass TACACS+ server authentication and login to OpenSwitch
   with allow-fail-through disabled

#### Test Fail Criteria
1. User mario failed to login after provide password three times
2. User mario able to login to OpenSwitch



## Test local authentication with fail-through

### Objective
This test case validates if user able to login to switch with local authentication and
fail-through enabled.


### Requirements
- Docker: up-to-date OpenSwitch docker image and pre-configured openswitch/tacacs_server image
- Physical: AS5712 switch loded with up-to-date OpenSwitch image, two TACACS+ servers


### Setup

#### Topology diagram
```ditaa
+----------+   +----------+   +----------+
|  Host 1  +---+  Switch  +---+  Host 2  |
+----------+   +----------+   +----------+
```
#### Test Setup

##### TACACS+ server setup
1. Disable TACACS+ service on two hosts
```
service tac_plus stop
```
2. Configure passkey(authentication key) on both host, passkey should show up in
   **/etc/tacacs/tac_plus.conf** as following:
```
key = "tac_test"
```
3. Create user mario on host 2, mario should show up in **/etc/tacacs/tac_plus.conf** as following:
```
  user = mario {
        pap = cleartext super
        service = exec {
         priv-lvl = 15
        }
  }
```
4. Enable TACACS+ service on two hosts
```
service tac_plus start
```

##### Authentication client (OpenSwitch) setup
1. Get ip address of two hosts
2. Configure the switch as TACACS+ authentication client and add two TACACS+ hosts
```
configure terminal
tacacs-server host 172.17.0.2 key tac_test
tacacs-server host 172.17.0.3 key tac_test
aaa group server tacacs+ sg1
(config-sg) server 172.17.0.2
exit
aaa group server tacacs+ sg2
(config-sg) server 172.17.0.3
exit
aaa authentication login default group local sg1 sg2
```
3. After verified local authentication success, change local group priority,
   then enable/disable fail-through
```
configure terminal
aaa authentication login default group sg1 local sg2
aaa authentication allow-fail-through
```
```
configure terminal
aaa authentication login default group sg1 sg2 local
aaa authentication allow-fail-through
```

### Description
User should be able to pass local authentication and login to switch use
username/password configured on switch with fail-through enabled regardless
local group priority


### Test result criteria

#### Test pass criteria
Local user netop (password: netop) able to pass local authentication and login to OpenSwitch

#### Test Fail Criteria
Local user netop failed to login after provide password three times
