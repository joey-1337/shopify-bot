#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

pip3 install requests
pip3 install json
pip3 install py-mini-racer
pip3 install lxml

