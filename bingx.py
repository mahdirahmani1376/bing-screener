import json
import time
import requests
import hmac
from hashlib import sha256
import pandas as pd
import json
from datetime import datetime,timedelta
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import ta
from tqdm import tqdm
import os

APIURL = "https://open-api.bingx.com";
defaultCurrenCyParamsMap = {
    "symbol": "BTC-USDT",
    "interval": "1d",
    # "startTime": str(int((datetime.now() - timedelta(days=1)).)),
    # "startTime": f"{0}",
    # "startTime": 5,
    # "startTime": 0,
    # "endTime": 0,
    # "limit": 0
}

defaultColumns = [
        "candlestick_chart_open_time",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "candlestick_chart_close_time",
        "Volume"
    ]
# serverRawTime = json.loads(getServerTime())["timestamp"]
# currentServerTime = convertToTimeStamp(serverRawTime)

##################################################################################################
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    # print("sign=" + signature)
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
###################################################################################################################
def getAllCurrencies():
    payload = {}
    path = '/openApi/spot/v1/common/symbols'
    method = "GET"
    paramsMap = {
    "symbol": ""
}
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def getCurrency(paramsMap):
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = "GET"

    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def convertToTimeStamp(x):
    timeoftest = datetime.utcfromtimestamp(float(x/1000))
    timeoftest = timeoftest + timedelta(hours=4)
    return timeoftest

def getServerTime():
    payload = {}
    path = '/api/v1/common/server/time'
    method = "GET"
    paramsMap = {}
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def showCandleStickChart(dataframe):
    candlestick = go.Candlestick(
                            x=dataframe.index,
                            open=dataframe['Open'],
                            high=dataframe['High'],
                            low=dataframe['Low'],
                            close=dataframe['Close']
                            )

    fig = go.Figure(data=[candlestick])

    fig.show()

def strongBullishCandle(row):
    return (row['Close'] >= row['High'] * 0.99) and (row['Close'] > row['Open'])
def strongBerishCandle(row):
    return (row['Close'] >= row['Low'] * 0.99) and (row['Close'] < row['Open'])
###################################################################################################################

# dfAllCurrencies = pd.json_normalize(json.loads(getAllCurrencies())['data']['symbols'])

def getCurrencyDataFrame(currencyParams):
    dfCurrency = pd.DataFrame(json.loads(getCurrency(currencyParams))['data'])
    ##########################################normalizing data###########################################################
    dfCurrency.columns = defaultColumns
    dfTimeStamp = dfCurrency.copy()
    dfTimeStamp['symbol'] = currencyParams['symbol']
    dfTimeStamp['candlestick_chart_close_time'] = dfTimeStamp['candlestick_chart_close_time'].apply(convertToTimeStamp)
    dfTimeStamp['candlestick_chart_open_time'] = dfTimeStamp['candlestick_chart_open_time'].apply(convertToTimeStamp)
    dfTimeStamp['Volume'] = dfTimeStamp['Volume'].apply(lambda x: x / 1000000)
    dfTimeStamp2 = dfTimeStamp.iloc[1:]
    dfTimeStamp2 = dfTimeStamp.set_index('candlestick_chart_close_time')
    ##########################################normalizing data###########################################################
    dfTimeStamp2['strong_bullish'] = dfTimeStamp2.apply(strongBullishCandle, axis=1)
    dfTimeStamp2['symbol'] = currencyParams['symbol']
    dfVolume = dfTimeStamp2.copy()
    dfVolume['last_day_volume'] = dfVolume['Volume'].shift(periods=-1)
    dfVolume['strong_volume'] = dfVolume.apply(lambda x: x['Volume'] > x['last_day_volume'], axis=1)
    # finalDF = dfVolume.iloc[[1][:]]
    # return dfTimeStamp2.iloc[1:2]
    return dfVolume

ScreenerDf = pd.DataFrame([],columns=defaultColumns,index=['candlestick_chart_close_time'])
threeDaysAgo = datetime.now() - timedelta(days=3)
threeDaysAgoInteger = int(threeDaysAgo.timestamp() * 1000)
test = []
# for i in tqdm(dfAllCurrencies['symbol']):
#     currencyParams = {
#     "symbol": f"{i}",
#     "interval": "1d",
#     # "startTime": f"{1691769599999}",
#     # "startTime": 1693238400000,
#     "startTime": thregetCurrencyDataFrameeDaysAgoInteger,
#     # "endTime": 1693497600000,
#     }
#     try:
#         dfCurrency = getCurrencyDataFrame(currencyParams)
#         test.append(dfCurrency)
#     except Exception as e:
#         print(e)
#         pass


# test2 = pd.concat(test)


# with pd.ExcelWriter(r"C:\Users\acer\Desktop\screener_data.xlsx") as writer:
#     test2.to_excel(writer)
symbol = 'CYBER-USDT'
currencyParams = {
    "symbol": symbol,
    "interval": "1d",
    # "startTime": threeDaysAgoInteger,
}
testDf = getCurrencyDataFrame(currencyParams)