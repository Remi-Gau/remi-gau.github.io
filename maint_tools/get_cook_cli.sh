#! /bin/bash

# get cook cli and install it

wget https://github.com/cooklang/cookcli/releases/download/v0.10.0/cook-x86_64-unknown-linux-gnu.tar.gz
tar -xvzf cook-x86_64-unknown-linux-gnu.tar.gz
rm cook-x86_64-unknown-linux-gnu.tar.gz
chmod +x cook

sudo mv cook /usr/local/bin/

cook --version
