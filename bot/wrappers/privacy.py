#API-wrapper the virtual credit card provider Privacy
# for more information visit https://privacy.com/developer/docs
#does not implement any of the sandbox only functions.

import json
import requests

url = "https://sandbox.privacy.com"
api_key = input("input privacy API-key")
headers = {'Authorization': 'api-key' + api_key,}


def _response_handler (response):
    response = response.json()

    if "message" in response:
        raise Exception(response["message"])
    else: 
        return response 


def list_cards (): return _response_handler(requests.get(url + '/v1/card', headers=headers))

def list_transactions (approval_status=None): 
    if approval_status:
        return _response_handler(requests.get(url + "v1/transaction/"))
    else:
        return _response_handler(requests.get(url + "v1/transaction/" + approval_status))

def create_card (type, memo=None, funding_token=None, pin=None, spend_limit_ammount=None, spend_limit_duration=None, state=None,shipping_address=None):
   
    payload = {"type":type}

    if memo: 
        payload = dict(payload, **{"memo":memo})
    
    if funding_token: 
        payload = dict(payload, **{"funding_token":funding_token})
    
    if pin and type == "PHYSICAL": 
        payload = dict(payload, **{"pin":pin})
    
    elif pin and type != "PHYSICAL": 
        raise Exception("pin attribute is only available for card with type PHYSICAL")

    if spend_limit_ammount: 
        payload = dict(payload, **{"spend_limit_ammount":spend_limit_ammount})

    if spend_limit_duration: 
        payload = dict(payload, **{"spend_limit_duration":spend_limit_duration})

    if state: 
        payload = dict(payload, **{"state":state})

    if shipping_address and type == "PHYSICAL": 
        payload = dict(payload, **{"shipping_address"})
    
    elif pin and type != "PHYSICAL":
        raise Exception("pin attribute is only available for card with type PHYSICAL")

    return _response_handler(requests.post(url + "/v1/card", json=payload, headers=headers))

def update_card(card_token, state=None,funding_token=None,memo=None,pin=None,spend_limit=None, spend_limit_duration=None):

    payload = {"card_token":card_token}

    if state: 
        payload = dict(payload, **{"state":state})

    if funding_token: 
        payload = dict(payload, **{"funding_token":funding_token})

    if memo: 
        payload = dict(payload, **{"memo":memo})

    if pin: 
        payload = dict(payload, **{"pin":pin})
    
    if spend_limit:
        payload = dict(payload, **{"spend_limit":spend_limit})
    
    if spend_limit_duration:
        payload = dict(payload, **{"spend_limit_duration":spend_limit_duration})

    return _response_handler(requests.put(url + "/v1/card", json=payload, headers=headers))


def reissue_card (card_token, shipping_address=None):

    payload = {"card_token":card_token}

    if shipping_address: 
        payload = dict(payload, **{"shipping_address":shipping_address})
    
    return _response_handler(requests.post(url + "/v1/card/reissue", json=payload, headers=headers))


def list_funding_accounts (source=None):

    if not source:
        return _response_handler(requests.get(url + "v1/fundingsource", headers=headers))
    
    elif source == "bank":
        return _response_handler(requests.get(url + "v1/fundingsource/bank", headers=headers))
    elif source == "card":
        return _response_handler(requests.get(url + "v1/fundingsource/card", headers=headers))
    else: raise Exception("not a valid source of funding")
    
