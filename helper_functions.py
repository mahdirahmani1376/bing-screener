import json
import time
import requests
import hmac
from hashlib import sha256
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# import ta
from tqdm.asyncio import tqdm
import os
import aiohttp
import asyncio
from aiolimiter import AsyncLimiter

weekly_time_frame = "1w"
h4_time_frame = "4h"
h1_time_frame = "1h"
d1_time_frame = "1d"
m_15_time_frame = '15m'
time_frame = weekly_time_frame

with open('credentials.json') as file:
    jsonFile = json.load(file)
    APIKEY = jsonFile['API_KEY']
    SECRETKEY = jsonFile['SECRET_KEY']

APIURL = "https://open-api.bingx.com"
timeStampFormat = '%Y-%m-%d %H:%M:%S'

MAX_CONCURRENT = 16
RATE_LIMIT_IN_SECOND = 16
limiter = AsyncLimiter(RATE_LIMIT_IN_SECOND, 1.0)

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
def calculate_percent_change(df,target,close_column_loc):
    if target not in range(len(df.index)):
        return False

    now = df.iloc[0, close_column_loc]
    target = df.iloc[target, close_column_loc]
    return ((now - target) / target) * 100

def convertToTimeStamp(x):
    timeoftest = datetime.utcfromtimestamp(float(x / 1000))
    timeoftest = timeoftest + timedelta(minutes=(3 * 60) + 30)
    timeoftest = timeoftest.strftime(timeStampFormat)
    return timeoftest


def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    # print("sign=" + signature)
    return signature


def praseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr + "&timestamp=" + str(int(time.time() * 1000))


###################################################################################################################
def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    # print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text


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
    return strongBullishSignal(row) and (row['last_day_close'] - row['last_day_close'] * 0.05) < row['open'] < (
            row['last_day_close'] + row['last_day_close'] * 0.05)


def openBelowLastDayClose(row):
    return row['open'] < row['last_day_open']


def bullishCloseAbovePastBars(index, df, value):
    return value > df.iloc[index + 1, index + 20]['close'].max


def strongCandle(row):
    return strongEngulf(row) and strongBody(row)


def strongBearishSignal(row):
    return strongCandle(row) and strongBerishCandle(row) and spikeBearishCandle(row)


def strongBullishSignal(row):
    return strongCandle(row) and strongBullishCandle(row) and spikeBullishCandle(row)


def strongBody(row):
    return abs(row['close'] - row['open']) > (abs(row['high'] - row['low']) / 3)


def strongCloseCandle(row):
    return (row['close'] >= row['high'] * 0.99) or (row['close'] >= row['low'] * 0.99)


def strongBullishCandle(row):
    try:
        return (row['close'] >= row['high'] * 0.99) and (row['close'] > row['open'])
    except:
        return (row['close'][0] >= row['high'][0] * 0.99) and (row['close'][0] > row['open'][0])


def spikeBullishCandle(row):
    return row['close'] > row['last_day_low'] + 3 * (row['last_day_close'] - row['last_day_low']) and row['close'] > (
        row['last_day_high'])


def spikeBearishCandle(row):
    return row['close'] < row['last_day_high'] - 3 * (row['last_day_close'] - row['last_day_high']) and row['close'] < (
        row['last_day_high'])


def strongBerishCandle(row):
    return (row['close'] >= row['low'] * 0.99) and (row['close'] < row['open'])


def strongEngulf(row):
    return abs(row['close'] - row['open']) > abs(3 * (row['last_day_close'] - row['last_day_open']))


###################################################################################################################
def strongRatio(row):
    return row['close'] > row['last_day_low'] + 6 * (row['last_day_close'] - row['last_day_low'])


def saveCandleStickChart(dataframe, path):
    candlestick = go.Candlestick(
        x=dataframe.index,
        open=dataframe['open'],
        high=dataframe['high'],
        low=dataframe['low'],
        close=dataframe['close']
    )

    fig = go.Figure(data=[candlestick])
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")

    # fig.write_image(f"charts/{name}.png")
    fig.write_image(path, width=1920, height=1080)


def final_bullish_signal(df):
    return (
            True in df['atr_rating'].values
            and True in df['strong_bullish_signal'].values
            and True in df['strong_ratio'].values
            and True in df['strong_bullish_close_past_bars_before'].values
            and df['adx_rating'].values[0] > 0
    )


def final_bearish_signal(df):
    return (
            True in df['atr_rating'].values
            and True in df['strong_bearish_signal'].values
            and True in df['strong_ratio'].values
            and True in df['strong_bearish_close_past_bars_before'].values
            and df['adx_rating'].values[0] < 0
    )


def getSavePath(savePath, dfFinal):
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    return os.path.join(savePath,
                        # f"{dfFinal['symbol'].values[0]}_cm_{dfFinal['crypto_meter_data'].values[0]}_cmc_"
                        f"{dfFinal['symbol'].values[0]}_cmc_"
                        f"{dfFinal['volume_coin_mcap'].values[0]}_rank{dfFinal['rank'].values[0]}.png")
