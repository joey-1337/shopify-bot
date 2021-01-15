#! /usr/bin/python

import json
import requests
from lxml import etree
import py_mini_racer
from io import StringIO
import multiprocessing

def get_root_node (session, url, parser, base_headers, referer=None):
    
    headers = dict(base_headers, **{"host":get_host(url)})
    if (referer != None): headers = dict(headers, **{"referer":referer})
    r = session.get(url, headers=headers, cookies=session.cookies)
    html = r.text
    tree = etree.parse(StringIO(html), parser)
    root = tree.getroot()
    return (root, r.url)

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
        print node, " ", node.text
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

def parse_css (css, url, session, cookies, headers, host, fonts_cache=None): #only parsing nested for nested stylesheets atm... may add fonts in future
    sheets = []
    index = 0
    try:
        while (True):
            begin = css[index:].index("@import")
            index = css[begin:].index(");") + begin
            nested_url = parse_url(css[begin + 13:index], url)
            r = request_from_html(session, cookies, headers, nested_url, host)
            sheets += [(r, nested_url)]
            sheets += parse_css(r.text, nested_url, session)
    except ValueError: 
        return sheets

def parse_url (href, url):
    if (href[0:4] == "http"): return href
    elif (href [0:2] == "//"): return "https:" + href
    else: return url + "/" + href


external_relations = ["shortcut icon"]

def get_host(url):
    host = url[url.index(":") + 3:]
    try:
        host = host = host[:host.index("/")]
    except ValueError: pass
    return host

def request_from_html (session, cookies, headers, url, host):
    url_host = get_host(url)
    if (url_host != host):
        return session.get(url, cookies = session.cookies, headers=dict(headers, **{"host":url_host}) )
    else:
        return session.get(url, cookies = session.cookies, headers=dict(headers, **{"host":host}))


def render (root, session, url, base_headers, external_rels=external_relations):
    
    host = get_host(url)
    headers = dict(base_headers, **{"referer":url})
    cookies = session.cookies

    external_requests = []
    #fonts_cache = [] add later
    node = root
    while (node != None):
        try:
            if (node.tag == "link" and node.attrib["rel"] == "stylesheet"):
                css_url = parse_url (node.attrib["href"], url)
                r = request_from_html (session, cookies, headers, css_url, host)
                external_requests += [(r, css_url)]
                external_requests += parse_css(r.text, css_url, session, cookies, headers, host)
            
            elif (node.tag == "link" and node.attrib["rel"] in external_relations):
                req_url = parse_url (node.attrib["href"], url)
                r = request_from_html (session, cookies, headers, req_url, host)
                external_requests += [(r, r.url)]
            
            elif (node.tag == "div" and node.attrib["style"][0:17] == "background-image:"):
                req_url = "https:" + node.attrib["style"][string.index("url") + 4:string.index(");")]
                r = request_from_html (session, cookies, headers, req_url)
                external_requests += [(r, r.url)]
        
            elif (node.tag == "img"):
                req_url = parse_url (node.attrib["src"], url)
                r = request_from_html (session, cookies, headers, req_url, host)
                external_requests += [(r, r.url)]

        except KeyError: pass 
        node = _iter(node)

    return external_requests
    #return root






