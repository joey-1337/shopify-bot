import json
import requests
from lxml import etree
from py_mini_racer import py_mini_racer
from io import StringIO
import cssutil

def get_root_node (session, url, parser, cookies=None, headers=None, data=None):
    r = session.get(url, headers=headers, cookies=cookies)
    html = r.text
    tree = etree.parse(StringIO(html), parser)
    root = tree.getroot()
    return root

def _iter (node): #gets next sequential dom node
    children = list(node)
    if (len(children) != 0):
        node = children[0]
    else:
        nextNode = node.getnext()
        if (nextNode != None):
            node = nextNode
        else:
            parent = node.getparent()
            uncle = parent.getnext()
            while (uncle == None):
                broken = False
                node = node.getparent()
                parent = node.getparent()
                if (parent == None):
                    return None
                uncle = parent.getnext()
            node = uncle
    return node

def print_dom_tree (root): #solely for testing purposes
    node = root
    while (node != None):
        print node, "", node.text
        node = _iter (node)

def get_elements_by_tag (root, tag):
    node = root
    elems = []
    while (node != None):
        if (node.tag == tag): elems += [node]
        node = _iter (node)
    return elems

def get_elements_by_attribute (root, attribute, value=None):
    node = root
    elems = []
    while (node != None):
        try:
            val = node.attrib[attribute]
            if (value):
                if (val == value): elems += [node]
            else:
                elems += [node]
        except KeyError: pass
        node = _iter(node)
    return elems                

def parse_css (css): pass


external_relations = ["stylesheet"]

def render (root, session, js_engine=None, cookies=None, headers=None, data=None):
    node = root
    while (node != None):
        try:

            if (node.tag == "link" and node.attrib["rel"] in external_relations):
                href = node.attrib["href"]
                if (href[0:4] == "http"):
                    session.get(href)
                    print "getting " + node.attrib["rel"] + " from: " + href
                else:
                    session.get("https:" + href)
                    print "getting " + node.attrib["rel"] + " from: https:" + href
            elif (node.tag == "div" and node.attrib["style"][0:17] == "background-image:"):
                session.get("https:" + node.attrib["style"][string.index("url") + 4:string.index(");")])
                print "getting bg image from " + "https:" + node.attrib["style"][string.index("url") + 4:string.index(");")]
        except KeyError: pass 
        node = _iter(node)
    return root






