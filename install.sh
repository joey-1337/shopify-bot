#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "[!] Please run as root"
  exit
fi

if ! command -v python &> /dev/null
then
    echo "[!] please install python onto your system"
    exit
fi

if ! command -v pip3 &> /dev/null
then
    echo "[!] please install pip3"
    exit
fi

echo "[*] installing python dependancies"

pip3 install requests
pip3 install py-mini-racer
pip3 install lxml
pip3 install cssutils
