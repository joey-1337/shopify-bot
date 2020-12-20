import json
import requests
from lxml import etree
from py_mini_racer import py_mini_racer
from io import StringIO

parser = etree.HTMLParser()


def generate_dom_tree (session, url): #solely for testing purposes
    r = session.get(url)
    html = r.text
    tree   = etree.parse(StringIO(html), parser)
    node = tree.getroot()
    
    while (True):
        broken = False               
        children = node.getchildren()
        if (len(children) != 0):   
            node = children[0]   
            print node, "", node.text
        else:                      
            nextNode = node.getnext()
            if (nextNode != None): 
                node = nextNode           
                print node, "", node.text     
            else:     
                parent = node.getparent()  
                uncle = parent.getnext()   
                while (uncle == None):
                    broken = False
                    node = node.getparent()
                    parent = node.getparent()
                    if (parent == None): 
                        broken = True
                        break
                    uncle = parent.getnext()
                if (broken): break  
                node = uncle
                print node, "", node.text 

