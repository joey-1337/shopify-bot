#!/bin/bash

#TODO pester the pmr devs to make their extensions work on the current version
#pray for success and a bountiful grain harvest
#find the newest combination of versions that 
#works
#strip libv8.so of unreferenced symbols... maybe, not exacly urgent

if [ "$EUID" -ne 0 ]
then 
    echo "[!] please run as root"
fi

echo -e "this script will download and create multiple files/folders in this repos parent folder so you probably don't want to run this script on your Desktop folder would you like to install in this given location [y/N]:\c"
read response 

if ["$response" -ne "y"] && ["$response" -ne "Y"]
then 
    exit
fi

cd ..

mkdir build

set -e

REPO_DIR=$(pwd)

PY_MINI_RACER_VERSION=0.1.17
V8_VERSION=6.7.288.46.1
URL=https://rubygems.org/downloads/libv8-$V8_VERSION-x86_64-linux.gem

echo "please note that until further notice... this script will take a very long time to run... furthermore, it will take up a lot of disk space (~4gb). Also, please make sure that g++ is up to date, otherwise it may be incapable of compiling some required v8 code."

if [ "$EUID" -ne 0 ]
then echo "[!] Please run as root"
  exit
fi

if ! command -v python &> /dev/null
then
    echo "[!] please install python onto your system"
    exit
fi

if ! command -v pip &> /dev/null
then
    echo "[!] please install pip"
    exit
fi

if ! command -v git &> /dev/null
then 
    echo "[!] please install git onto your system"
    exit
fi

echo "[*] getting C++ dependancies"

cd ..
wget https://github.com/pmed/v8pp/archive/v1.6.0.zip
unzip v1.6.0.zip
rm v1.6.0.zip

echo "[*] installing python dependancies"

pip install requests 
pip install lxml

#git clone https://github.com/sqreen/PyMiniRacer ideally in the future all these
#projects should sync up to the current version... but for now neither v8pp 
#not py_mini_racer can support that.

wget https://github.com/sqreen/PyMiniRacer/archive/0.1.17.zip
unzip 0.1.17.zip
rm 0.1.17.zip
cd PyMiniRacer-0.1.17

#this part is largely just the build_so.sh script from the py_mini_racer
#but executing the script directly wouldn't add the aditional dependancies
#so we have to reuse the code instead of just calling it.

echo "[*] modifying py_mini_racer to support require() statements"

REPLACE_TEXT='s#_ext_handle = ctypes.CDLL(EXTENSION_PATH)#_ext_handle = ctypes.CDLL("'"$REPO_DIR"'/build/_v8.so")#g'
sed "$REPLACE_TEXT" py_mini_racer/py_mini_racer.py > $REPO_DIR/build/py_mini_racer.py
cd ..
rm -r PyMiniRacer-0.1.17 #it's really unnecessary to keep the rest of the repo

echo "[*] building v8 shared objects"

echo "[*] getting libv8 developer files from ruby gem (don't ask)"

mkdir libv8-$V8_VERSION
cd libv8-$V8_VERSION

curl "$URL" --output libv8.gem
tar xvf libv8.gem
tar xvf data.tar.gz
rm metadata.gz checksums.yaml.gz data.tar.gz

echo "[*] building C++ dependancies"

cd ..
cd v8pp-1.6.0

echo "[*] altering makefile for v8pp"

#I don't remember which precise changes I made to the Makefile in order to get the 
#lib to properly compile so until I figure that out and implement a sed-like solution
#like I did for the mini_racer dependancy, this will have to do. 

#TODO make a function or something, idk...

LINE=2
DIFF="CXXFLAGS += -pthread -Wall -Wextra -std=c++11 -fPIC -fno-rtti -DV8PP_ISOLATE_DATA_SLOT=0 -g"
AWK_TEXT='{ if (NR == '"$LINE"') print "'"$DIFF"'"; else print $0}'
awk "$AWK_TEXT" Makefile > awk1.out
rm Makefile

LINE=7
DIFF="INCLUDES = -I ../libv8-$V8_VERSION/vendor/v8/include -I ../libv8-$V8_VERSION/vendor/v8 -I."
AWK_TEXT='{ if (NR == '"$LINE"') print "'"$DIFF"'"; else print $0}'
awk "$AWK_TEXT" awk1.out > awk2.out
rm awk1.out

LINE=8
DIFF="LIBS = -ldl -lrt  -licui18n -licuuc -L. -Wl,-whole-archive -lv8pp -ldl -lpthread -Wl,--start-group ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_monolith.a ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_libplatform.a  ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_libbase.a -Wl,--end-group"
AWK_TEXT='{ if (NR == '"$LINE"') print "'"$DIFF"'"; else print $0}'
awk "$AWK_TEXT" awk2.out > Makefile
rm awk2.out

make lib

cp $REPO_DIR/bot/html-parser/dom-parser/js-objects/racer_plus.cc .

#the file gets linked against half of my computer's file system
#I'd honestly be more surprised if there was a linker error than not

g++ \
    -g -O2\
    -I.\
    -I ../libv8-$V8_VERSION/vendor/v8/include\
    -I ../libv8-$V8_VERSION/vendor/v8\
    racer_plus.cc\
    -o _v8.so\
    -Wl,--start-group libv8pp.a ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_monolith.a ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_libplatform.a  ../libv8-$V8_VERSION/vendor/v8/out.gn/libv8/obj/libv8_libbase.a \
    -Wl,--end-group \
    -std=c++0x \
    -DV8_COMPRESS_POINTERS \
    -ldl \
    -lrt \
    -pthread \
    -shared \
    -fno-rtti \
    -fPIC

cp _v8.so $REPO_DIR/build

cd $REPO_DIR/..
chown -R $(logname) $(pwd)

