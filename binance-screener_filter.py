import asyncio
import os.path
import requests
import pandas as pd
from bingx_spot_list import get_spot_df
from helper_functions import convertToTimeStamp
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from tqdm.asyncio import tqdm
import os
import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
from datetime import datetime

MAX_CONCURRENT = 16
RATE_LIMIT_IN_SECOND = 16
limiter = AsyncLimiter(RATE_LIMIT_IN_SECOND, 1.0)

url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}
symbols_url = 'https://api.binance.com/api/v3/exchangeInfo'

weekly_time_frame = "1w"
h4_time_frame = "4h"
h1_time_frame = "1h"
d1_time_frame = "1d"
m_15_time_frame = '15m'
time_frame = h4_time_frame

response_binance_list = requests.get(symbols_url, headers=headers).json()
df_binance = pd.DataFrame(response_binance_list['symbols'])
df_binance_pairs = df_binance[(df_binance['quoteAsset'] == 'USDT') & (df_binance['status'] == 'TRADING')]
df_binance_pairs = df_binance_pairs[df_binance_pairs['baseAsset'] != 'BTC']
df_binance_pairs = df_binance_pairs[df_binance_pairs['baseAsset'] != 'USDC']
df_binance_pairs = df_binance_pairs[df_binance_pairs['baseAsset'] != 'TUSD']


def generate_sub_plot(df_usdt, df_btc, file_name):
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    candlestick = go.Candlestick(
        x=df_usdt.index,
        open=df_usdt['open'],
        high=df_usdt['high'],
        low=df_usdt['low'],
        close=df_usdt['close'],
        name='usdt'
    )
    candlestick_btc = go.Candlestick(
        x=df_btc.index,
        open=df_btc['open'],
        high=df_btc['high'],
        low=df_btc['low'],
        close=df_btc['close'],
        name='btc',
    )

    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(candlestick_btc, row=2, col=1)
    fig.update_layout(
        template="plotly_dark",
        autosize=True
    )
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_yaxes(type='log')

    now = datetime.now().strftime('%Y-%m-%d')
    path = f"charts/binance/{time_frame}/{now}"
    if not os.path.exists(path):
        os.makedirs(path)
    fig.write_image(os.path.join(path, f"{file_name}.png"), width=1920, height=1080)


async def main(df_binance_pairs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in (df_binance_pairs.itertuples()):
            base_asset = i[df_binance_pairs.columns.get_loc('baseAsset') + 1]
            usdt_pair = str(base_asset) + "USDT"
            btc_pair = str(base_asset) + 'BTC'
            if btc_pair in df_binance['symbol'].values:
                usdt_symbol_url = f"https://api.binance.com/api/v3/klines?symbol={usdt_pair}&interval={time_frame}"
                btc_symbol_url = f"https://api.binance.com/api/v3/klines?symbol={btc_pair}&interval={time_frame}"

                tasks.append(
                    asyncio.ensure_future(
                        sendAsyncRequest(session, base_asset, usdt_pair, btc_pair, usdt_symbol_url, btc_symbol_url)))

        results = []
        for f in tqdm.as_completed(tasks, total=len(tasks)):
            results.append(await f)

        return results


def transform_dataframe(response, name):
    df = pd.DataFrame(response)
    columns = [
        "candlestick_chart_open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "candlestick_chart_close_time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Unused field"
    ]
    df.columns = columns
    df['symbol'] = name
    df['candlestick_chart_close_time'] = df['candlestick_chart_close_time'].apply(
        convertToTimeStamp)
    df['candlestick_chart_open_time'] = df['candlestick_chart_open_time'].apply(
        convertToTimeStamp)
    df = df.set_index('candlestick_chart_close_time').sort_index(ascending=True)
    change_last_day = float(df['close'].values[0]) - float(df['close'].values[6])
    change_last_week = float(df['close'].values[0]) - float(df['close'].values[24])
    return (df, change_last_week, change_last_day)


async def sendAsyncRequest(session, base_asset, usdt_pair, btc_pair, usdt_symbol_url, btc_symbol_url):
    # async with limiter:
    try:
        async with limiter:
            async with session.get(usdt_symbol_url) as response:
                text = await response.json()
                df_usdt, usdt_change_last_week, usdt_change_last_day = transform_dataframe(text, usdt_pair)

        async with limiter:
            async with session.get(btc_symbol_url) as response:
                text = await response.json()
                df_btc, btc_change_last_week, btc_change_last_day = transform_dataframe(text, btc_pair)

        if (btc_change_last_day < 0 and usdt_change_last_day > 0) or (btc_change_last_week < 0 and usdt_change_last_week > 0):
            return generate_sub_plot(df_usdt, df_btc, usdt_pair)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main(df_binance_pairs))
