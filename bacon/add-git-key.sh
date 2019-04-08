wget https://raw.githubusercontent.com/chenjianAgain/cv/master/bacon/key.pri
rm -rf ~/.ssh/id_rsa
touch ~/.ssh/id_rsa
chmod 777 ~/.ssh/id_rsa
cat key.pri > ~/.ssh/id_rsa
chmod 400 ~/.ssh/id_rsa
