import requests

#TODO: generate checkout url with dummy product
#checkout


base_cookies ={
'cart_currency': 'USD',
'secure_customer_sig': '',
'_shopify_country': 'United+States',
'_orig_referrer': 'https%3A%2F%2Fkith.com%2F',
'_landing_page': '%2Fproducts%2Fnkcj0609-700%3Fvariant%3D19438822621312',
'shopify_pay_redirect': 'pending',
'GlobalE_Data': '%7B%22countryISO%22%3A%22US%22%2C%22currencyCode%22%3A%22USD%22%2C%22cultureCode%22%3A%22en-US%22%7D',
'_shopify_sa_p': '',
'GlobalE_SupportThirdPartCookies': 'true',
'GlobalE_Full_Redirect': 'false',
'cart_ver': 'gcp-us-central1%3A1',
'_shopify_sa_t': '2020-12-06T02%3A38%3A29.207Z', 
'acceptedCookies': 'yes',
}

base_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://kith.com',
    'Connection': 'keep-alive',
    'Referer': 'https://kith.com/products/nkcj0609-700?variant=19438822621312',
    'TE': 'Trailers',
}


def add_to_cart(user_agent, id, size):

  headers = dict(base_headers, **{"user-agent":user_agent})
  data = {
    'properties[upsell]': 'mens',
    'option-0': size,
    'id': size,
    'quantity': '1'
  }
  response = requests.post('https://kith.com/cart/add.js', headers=headers, cookies=cookies, data=data)
  return response


