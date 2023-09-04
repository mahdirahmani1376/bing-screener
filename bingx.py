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
from tqdm.asyncio import tqdm
import os
import aiohttp
import asyncio
from aiolimiter import AsyncLimiter

MAX_CONCURRENT = 8
RATE_LIMIT_IN_SECOND = 8
limiter = AsyncLimiter(RATE_LIMIT_IN_SECOND, 1.0)
h4_time_frame = "4h"
h1_time_frame = "1h"
d1_time_frame = "1d"
time_frame = h4_time_frame

with open('credentials.json') as file:
    jsonFile = json.load(file)
    APIKEY = jsonFile['API_KEY']
    SECRETKEY = jsonFile['SECRET_KEY']

APIURL = "https://open-api.bingx.com"

timeStampFormat = '%Y-%m-%d %H:%M:%S'
# lastDay = (datetime.now() - timedelta(days=1)).strftime(timeStampFormat)

defaultCurrenCyParamsMap = {
    "symbol": "BTC-USDT",
    "interval": f"{time_frame}",
}

defaultColumns = [
        "candlestick_chart_open_time",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "candlestick_chart_close_time",
        "volume"
    ]
# serverRawTime = json.loads(getServerTime())["timestamp"]
# currentServerTime = convertToTimeStamp(serverRawTime)

async def main(dfAllCurrencies):
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = "GET"
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in (dfAllCurrencies['symbol']):
            currencyParams = {
                "symbol": f"{i}",
                "interval": f"{time_frame}",
                "startTime": startTime,
            }
            paramsStr = praseParam(currencyParams)
            tasks.append(asyncio.ensure_future(sendAsyncRequest(session,path,paramsStr,currencyParams = currencyParams)))

        results = []
        # results = await asyncio.gather(*tasks)
        for f in tqdm.as_completed(tasks,total=len(tasks)):
            results.append(await f)

        return results
async def sendAsyncRequest(session, path, urlpa,currencyParams):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    async with limiter:
        try:
            async with session.get(url) as response:
                text =  await response.text()
                return getCurrencyDataFrame(text,currencyParams)
        except Exception as e:
            print("first error in send request loop")
            print(e)
##################################################################################################
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    # print("sign=" + signature)
    return signature

def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    # print(url)
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
    timeoftest = timeoftest + timedelta(minutes=(4*60)+30)
    timeoftest = timeoftest.strftime(timeStampFormat)
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
                            open=dataframe['open'],
                            high=dataframe['high'],
                            low=dataframe['low'],
                            close=dataframe['close']
                            )

    fig = go.Figure(data=[candlestick])

    fig.show()
def strongBullishSignalBar(row):
    return strongBullishSignal(row) and (row['last_day_close'] - row['last_day_close'] * 0.05) < row['open'] < (row['last_day_close'] + row['last_day_close'] * 0.05)

def openBelowLastDayClose(row):
    return row['open'] < row['last_day_open']

def bullishCloseAbovePastBars(index,df,value):
    return value > df.iloc[index+1,index+20]['close'].max
def strongCandle(row):
    return strongEngulf(row) and strongBody(row)

def strongBearishSignal(row):
    return strongCandle(row) and strongBerishCandle(row) and spikeBearishCandle(row)

def strongBullishSignal(row):
    return strongCandle(row) and strongBullishCandle(row) and spikeBullishCandle(row)
def strongBody(row):
    return abs(row['close'] - row['open']) > (abs(row['high'] - row['low'])/3)
def strongCloseCandle(row):
    return (row['close'] >= row['high'] * 0.99) or (row['close'] >= row['low'] * 0.99)

def strongBullishCandle(row):
    return (row['close'] >= row['high'] * 0.99) and (row['close'] > row['open'])

def spikeBullishCandle(row):
    return row['close'] > row['last_day_low'] + 3 * (row['last_day_close'] - row['last_day_low'])

def spikeBearishCandle(row):
    return row['close'] < row['last_day_high'] - 3 * (row['last_day_close'] - row['last_day_high'])
def strongBerishCandle(row):
    return (row['close'] >= row['low'] * 0.99) and (row['close'] < row['open'])

def strongEngulf(row):
    return abs(row['close'] - row['open']) > abs(3 * (row['last_day_close'] - row['last_day_open']))

###################################################################################################################
def saveCandleStickChart(dataframe,path):
    candlestick = go.Candlestick(
                            x=dataframe.index,
                            open=dataframe['open'],
                            high=dataframe['high'],
                            low=dataframe['low'],
                            close=dataframe['close']
                            )

    fig = go.Figure(data=[candlestick])

    # fig.write_image(f"charts/{name}.png")
    fig.write_image(path)
###################################################################################################################

def getCurrencyDataFrame(data,currencyParams):
    dfCurrency = pd.DataFrame(json.loads(data)['data'])
    ##########################################normalizing data###########################################################
    dfCurrency.columns = defaultColumns
    dfTimeStamp = dfCurrency.copy()
    dfTimeStamp['symbol'] = currencyParams['symbol']
    dfTimeStamp['candlestick_chart_close_time'] = dfTimeStamp['candlestick_chart_close_time'].apply(convertToTimeStamp)
    dfTimeStamp['candlestick_chart_open_time'] = dfTimeStamp['candlestick_chart_open_time'].apply(convertToTimeStamp)
    dfTimeStamp['volume'] = dfTimeStamp['volume'].apply(lambda x: x / 1000000)
    dfTimeStamp2 = dfTimeStamp.set_index('candlestick_chart_close_time')
    ##########################################normalizing data###########################################################
    dfTimeStamp2['strong_bullish'] = dfTimeStamp2.apply(strongBullishCandle, axis=1)
    dfTimeStamp2['strong_bearish'] = dfTimeStamp2.apply(strongBerishCandle, axis=1)
    dfTimeStamp2['symbol'] = currencyParams['symbol']
    dfvolume = dfTimeStamp2.copy()
    dfvolume = dfvolume.sort_index(ascending=False)
    dfvolume['last_day_volume'] = dfvolume['volume'].shift(periods=-1)
    dfvolume['last_day_open'] = dfvolume['open'].shift(periods=-1)
    dfvolume['last_day_close'] = dfvolume['close'].shift(periods=-1)
    dfvolume['last_day_high'] = dfvolume['high'].shift(periods=-1)
    dfvolume['last_day_low'] = dfvolume['low'].shift(periods=-1)
    dfvolume['strong_volume'] = dfvolume.apply(lambda x: x['volume'] > 3 * (x['last_day_volume']), axis=1)
    dfvolume['strong_engulf'] = dfvolume.apply(strongEngulf,axis=1)
    dfvolume['strong_close'] = dfvolume.apply(strongCloseCandle, axis=1)
    dfvolume['strong_body'] = dfvolume.apply(strongBody, axis=1)
    dfvolume['strong'] = dfvolume.apply(strongCandle, axis=1)
    dfvolume['strong_bullish_signal'] = dfvolume.apply(strongBullishSignal, axis=1)
    dfvolume['strong_bearish_signal'] = dfvolume.apply(strongBearishSignal, axis=1)
    dfvolume['strong_bullish_signal_bar'] = dfvolume.apply(strongBullishSignalBar, axis=1)
    dfvolume['open_below_last_day_close'] = dfvolume.apply(openBelowLastDayClose, axis=1)

    strongBullishCloseList = []
    strongBearishCloseList = []
    for index, value in enumerate(dfvolume['close']):
        bullishValueToAppend = value > dfvolume.iloc[index + 1:index + 7]['close'].max()
        bearishValueToAppend = value < dfvolume.iloc[index + 1:index + 7]['close'].min()
        strongBullishCloseList.append(bullishValueToAppend)
        strongBearishCloseList.append(bearishValueToAppend)

    dfvolume['strong_bullish_close_past_bars_before'] = strongBullishCloseList
    dfvolume['strong_bearish_close_past_bars_before'] = strongBearishCloseList

    # saveImageCheck = True in dfvolume.iloc[0:7]['strong_engulf'].values
    # if saveImageCheck:
    #     path = f"charts/{currencyParams['symbol']}.png"
    #     saveCandleStickChart(dfvolume, path)

    with pd.ExcelWriter(f"data/{time_frame}/{currencyParams['symbol']}.xlsx") as dfVolumeWriter:
        dfvolume.to_excel(dfVolumeWriter)
    # return dfvolume

    return dfvolume.iloc[[1][:]]

if __name__ == '__main__':
    dfAllCurrencies = pd.json_normalize(json.loads(getAllCurrencies())['data']['symbols'])
    ScreenerDf = pd.DataFrame([], columns=defaultColumns, index=['candlestick_chart_close_time'])
    # startTime = datetime.now() - timedelta(days=30)
    startTime = datetime.now() - timedelta(days=7)
    startTime = int(startTime.timestamp() * 1000)
    results = asyncio.run(main(dfAllCurrencies))
    finalDf = pd.concat(results)

    with pd.ExcelWriter(r"screener_data_h4.xlsx") as writer:
        finalDf.to_excel(writer)
