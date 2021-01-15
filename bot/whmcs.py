from dom_parser import core as c
import requests
from lxml import etree
import random
import py_mini_racerr

def buy_product ():
     prod_name = raw_input("enter product name: ")
     url = "http://test.ccds.club/"
     parser = etree.HTMLParser()
     session = requests.session()
     headers = {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Language': 'en-US,en;q=0.5',
     'Referer': 'http://test.ccds.club/',
     'DNT': '1',
     'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
     }
     session = second_page(headers, requests.session(), url, parser, py_mini_racerr.MiniRacer(), prod_name)
     checkout(headers, session, parser, py_mini_racerr.MiniRacer())

def checkout(base_headers, session, parser, ctx):
     res =  c.get_root_node(session, "http://test.ccds.club/cart.php?a=view", parser, base_headers, referer="http://test.ccds.club/index.php?rp=/store/the-best-products")
     root = res[0];url = res[1]
     c.render(root, session, url, base_headers)
     c.get_root_node(session, "http://test.ccds.club/cart.php?a=checkout&e=false", parser, base_headers)
     root = res[0];url = res[1]
     c.render(root, session, url, base_headers)
     params = (('a', 'checkout'),)
     script = c.get_elements_by_tag(root, "script")[0]
     ctx.eval(script.text)
     csrfToken = str(ctx.eval("csrfToken"))
     data = {
     'token': csrfToken,
     'submit': 'true',
     'custtype': 'new',
     'loginemail': '',
     'loginpassword': '',
     'firstname': 'test',
     'lastname': 'test',
     'email': str(random.randint(1000,10000)) + '@gfake.com',
     'country-calling-code-phonenumber': '1',
     'phonenumber': '704-909-9305',
     'companyname': 'test',
     'address1': 'test',
     'address2': 'test',
     'city': 'test',
     'state': 'North Carolina',
     'postcode': '28277',
     'country': 'US',
     'password': 'JP@25SvC)sW1',
     'password2': 'JP@25SvC)sW1',
     'applycredit': '1',
     'paymentmethod': 'paypal',
     'ccinfo': 'new',
      'ccnumber': '',
     'ccexpirydate': '',
     'cccvv': '',
     'ccdescription': '',
     'notes': '',
     'marketingoptin': '1'
      }
     headers = dict(base_headers, **{"host":c.get_host(url)})
     headers = dict(headers, **{'Referer': 'http://test.ccds.club/cart.php?a=checkout'})
     r = session.post("http://test.ccds.club/cart.php",headers=headers, params=params, cookies=session.cookies, data=data)
     return r

def second_page(base_headers, session, url, parser, ctx, prod_name):
     headers = dict(base_headers, **{"host":c.get_host(url)})
     headers = dict(headers, **{"referer":"http://test.ccds.club/index.php"})
     session.get("http://test.ccds.club/cart.php")
     res = c.get_root_node(session, url + "index.php?rp=/store/the-best-products",parser,headers)
     root = res[0];
     url = "http://test.ccds.club/index.php?rp=/store/the-best-products"
     c.render(root, session, "http://test.ccds.club/index.php?rp=/store/the-best-products", base_headers)
 
     script = c.get_elements_by_tag(root, "script")[0]
     ctx.eval(script.text)
 
     csrfToken = str(ctx.eval("csrfToken"))
 
     for node in c.get_elements_by_tag(root, "strong"):
         if (node.text == prod_name): break
 
     
     prod_id = node.getprevious().attrib['id']
     data = {"token":csrfToken,"pid":prod_id[-1]}
 
     params = (('a', 'add'),)
     print "found product with ID:", prod_id, "and  token:", csrfToken
 
     session.post('http://test.ccds.club/cart.php', headers=headers, params=params, cookies=session.cookies, data=data)
     return session

