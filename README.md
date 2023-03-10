
## execution environment

- Ubuntu20.04
- Python3

### Required modules listed below
（Running requirements.sh runs the following command）

List the required modules on equirements.txt
```sh equirements.txt
$ apt install python3-pip

$ pip3 install numpy

$ pip3 install PyCryptodome

$ pip3 install websocket_server==0.4

↑Undoable without version specified

$ pip3 websocket_client

$ pip3 install plyvel

$ apt-get -y install python3-tk
```

## How to do it


It is necessary to set the IP address and PORT number in order to execute.

``` python3 APP/settings.py
Changing the IP Address(Line 1):HOST_IP_LAYER_0 = 'xx.xx.xxx.xx'
```

### Start the number of startup nodes according to the size of the P2P network you want to build

```sh
$ python3 owner_server0.py

$ python3 owner_server1.py

$ python3 owner_server2.py

$ python3 owner_server3.py

$ python3 owner_server4.py

        ・
        ・
        ・

$ python3 owner_serverXX.py <-(It is desirable to start in order)
```
