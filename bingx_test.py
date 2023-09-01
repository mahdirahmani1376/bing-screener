
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com";
APIKEY="RNwiGyrmRxytM2J6ggFx9nuBSr1MCLlDy2ZNBQ9XeH15rxizCyp6jv7L5XuGQ02efQxDwWWz0Y4H67AZajBGDQ"
SECRETKEY="6vxO1MMbutktJIDams1dxTAslFbV6DAS3ftQhMbCWqnyWouQSLsugcMXvetz8mtp5fjmfY2baZMcFmsewXg"

def demo():
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = "GET"
    paramsMap = {
    "symbol": "BTC-USDT",
    "interval": "",
    "startTime": 0,
    "endTime": 0,
    "limit": 0
}
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


if __name__ == '__main__':
    print("demo:", demo())
