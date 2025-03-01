#! /bin/bash

# get cook cli and install it

# if /usr/local/bin/cook already exists, return early
if [ -f /usr/local/bin/cook ]; then
    echo " cook already exists in /usr/local/bin/"
    echo " If you want to update cook, please remove it first with:"
    echo ""
    echo "   rm -f /usr/local/bin/cook"
    echo ""
    exit 0
fi

wget https://github.com/cooklang/cookcli/releases/download/v0.10.0/cook-x86_64-unknown-linux-gnu.tar.gz
tar -xvzf cook-x86_64-unknown-linux-gnu.tar.gz
rm cook-x86_64-unknown-linux-gnu.tar.gz
chmod +x cook

sudo mv cook /usr/local/bin/

cook --version

echo ""
