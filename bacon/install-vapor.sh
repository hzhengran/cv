#!/bin/bash
## install dependencies -- swift vapor
sudo apt-get update
sudo apt-get install -y clang
sudo apt-get install -y libcurl3 libpython2.7 libpython2.7-dev
wget https://swift.org/builds/swift-4.2.1-release/ubuntu1804/swift-4.2.1-RELEASE/swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
tar xzf swift-4.2.1-RELEASE-ubuntu18.04.tar.gz
sudo mv swift-4.2.1-RELEASE-ubuntu18.04 /usr/share/swift
echo "export PATH=/usr/share/swift/usr/bin:$PATH" >> ~/.bashrc
source  ~/.bashrc
sudo apt-get update && apt-get upgrade
sudo apt install -y curl
eval "$(curl -sL https://apt.vapor.sh)"
sudo apt-get install -y vapor
