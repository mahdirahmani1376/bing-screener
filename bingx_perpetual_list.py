import hmac
import json
import time
from hashlib import sha256

import pandas as pd
import requests

from helper_functions import APIKEY, SECRETKEY

APIURL = "https://open-api.bingx.com";

def demo():
    payload = {}
    path = '/openApi/swap/v2/quote/contracts'
    method = "GET"
    paramsMap = {}
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def praseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+"&timestamp="+str(int(time.time() * 1000))


def get_perpetual_df():
    response = json.loads(demo())
    return pd.DataFrame(response['data'])

