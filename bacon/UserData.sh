#!/bin/bash
## install dependencies -- swift vapor
mkdir a
sudo apt-get update
sudo apt-get install -y clang
sudo apt-get install -y libcurl3 libpython2.7 libpython2.7-dev
mkdir b
wget https://swift.org/builds/swift-4.2.1-release/ubuntu1804/swift-4.2.1-RELEASE/swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
tar xzf swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
sudo mv swift-4.2.1-RELEASE-ubuntu18.04 /usr/share/swift
mkdir chenjianAgain
echo "export PATH=/usr/share/swift/usr/bin:$PATH" >> ~/.bashrc
source  ~/.bashrc
mkdir c
sudo apt install -y curl
eval "$(curl -sL https://apt.vapor.sh)"
sudo apt-get install -y swift vapor
##swift --version
##vapor --help
mkdir d
## download source code from github
wget https://raw.githubusercontent.com/chenjianAgain/cv/master/bacon/key.pri
rm -rf ~/.ssh/id_rsa
touch ~/.ssh/id_rsa
chmod 777 ~/.ssh/id_rsa
cat key.pri > ~/.ssh/id_rsa
chmod 400 ~/.ssh/id_rsa
git clone git@github.com:derekcoder/AcronymApp.git
cd AcronymApp
mkdir e
## change db source
sed -i 's/localhost/35.238.101.198/g' Sources/App/configure.swift
mkdir f
## vapor build and run in background
vapor build 
nohup vapor run --hostname=0.0.0.0 --port=8080 &
