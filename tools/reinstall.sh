#!/bin/bash 

/bin/echo -e "[?] this script will delete and reinstall the this repo and all of its dependancies any unpushed changes will be lost. would you like to continue [y/N]:\c"
read response

if [["$response" -ne y] && ["$response" -ne Y]]
then
    exit 
fi

if [ "$EUID" -ne 0 ] 
then 
    echo "[!] please run as root"
    exit
fi

cd ../..
yes | rm -r libv8-*  shopify-bot  v8pp-1.6.0

git clone https://github.com/joey-1337/shopify-bot
cd shopify-bot/tools

yes | ./install.sh
