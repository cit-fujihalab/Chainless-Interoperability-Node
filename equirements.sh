
#!/bin/bash

command1="sudo apt install python3-pip"
command2="pip3 install numpy"
command3="pip3 install PyCryptodome"
command4="pip3 install websocket_server==0.4"
command5="pip3 install websocket_client"
command6="pip3 install plyvel"
command7="sudo apt-get -y install python3-tk"

eval $command1
eval $command2
eval $command3
eval $command4
eval $command5
eval $command6
eval $command7

