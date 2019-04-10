    sudo apt-get -q update
    sudo apt-get -q install -y wget software-properties-common python-software-properties apt-transport-https
    #wget -q https://repo.vapor.codes/apt/keyring.gpg -O- | $SUDO apt-key add -
    echo "deb https://repo.vapor.codes/apt bionic main" | sudo tee /etc/apt/sources.list.d/vapor.list
    sudo apt-get -q update
