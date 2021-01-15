#!/usr/bin/python
import whmcs

def bot ():
     master = {'http://test.ccds.club':whmcs.buy_product}
     domain = raw_input("enter website name: ")
     master[domain]()

