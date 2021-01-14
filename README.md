# shopify-bot
not even shopify based anymore... smh



## Installation

Installation have been tested on Arch Linux 2021.01.01-amd64 and Debian 10.7.0-amd64, MacOS and Windows support should be coming in the foresable future... everything should probably work fine on Mac if you have installed the required dependancies. The code should *theoretically* work on Windows if you compile it manually, but I have not tried it yet. Support for CPU architectures other than amd64 is not planned. Takes up ~ 90mb of space once installed, the install script should not take very long to execute.

__requirements to run install.sh__:
  - bash
  - python
  - pip
  - g++
  - git
  

Install with this simple oneliner... but **make sure you are doing it in an empty directory**.

`git clone https://github.com/joey-1337/shopify-bot && cd shopify-bot/tools && yes | sudo ./install.sh`

## dependencies 

the install.sh script handles all of these. Do not attempt to install py_mini_racer or v8pp, the script modifies both prior to use. 

__python__:
  - [py_mini_racer](https://github.com/sqreen/PyMiniRacer)
  - [lxml](https://lxml.de/)
  - [requests](https://requests.readthedocs.io/en/master/)
__c++__:
  - [v8pp](https://github.com/pmed/v8pp)
  - v8 [(binaries)](https://rubygems.org/gems/libv8/) [homepage](https://v8.dev/)
