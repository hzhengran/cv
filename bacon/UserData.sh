#!/bin/bash
## install dependencies -- swift vapor
sudo apt install -y update
sudo apt-get install -y clang curl
sudo apt-get install -y libcurl3 libpython2.7 libpython2.7-dev
wget https://swift.org/builds/swift-4.2.1-release/ubuntu1804/swift-4.2.1-RELEASE/swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
tar xzf swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
sudo mv swift-4.2.1-RELEASE-ubuntu18.04 /usr/share/swift
echo "export PATH=/usr/share/swift/usr/bin:$PATH" >> ~/.bashrc
source  ~/.bashrc
eval "$(curl -sL https://apt.vapor.sh)"
sudo apt-get install -y swift vapor
swift --version
vapor --help

## download source code from github
wget https://raw.githubusercontent.com/chenjianAgain/cv/master/bacon/key.pri
cat key.pri >> ~/.ssh/id_rsa
chmod 400 !$
git clone git@github.com:derekcoder/AcronymApp.git && cd AcronymApp

## change db source
sed -i 's/localhost/35.238.101.198/g' Sources/App/configure.swift

## vapor build and run in background
vapor build && nohup vapor run --hostname=0.0.0.0 --port=8080 &
