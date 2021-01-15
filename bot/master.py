#!/usr/bin/python
import dom_parser

def bot ():
     master = {'http://test.ccds.club':dom_parser.whmcs.buy_product}
     domain = raw_input("enter website name: ")
     master[domain]()

