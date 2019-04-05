#!/bin/bash

wget https://raw.githubusercontent.com/chenjianAgain/cv/master/bacon/install-vapor.sh
chmod +x install-vapor.sh
./install-vapor.sh

sudo su -
git clone https://github.com/chenjianAgain/VaporTest3.git
cd VaporTest3/
vapor build
nohup vapor run --hostname=0.0.0.0 --port=80 &
