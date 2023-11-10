import requests
import pandas as pd
from bingx_spot_list import get_spot_df
from helper_functions import convertToTimeStamp
import plotly.graph_objects as go
import matplotlib.pyplot as plt

url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}
symbols_url = 'https://api.binance.com/api/v3/exchangeInfo'

response_binance_list = requests.get(symbols_url, headers=headers).json()
df_binance_symbols = pd.DataFrame(response_binance_list['symbols'])['symbol'].values.tolist()
df_bingx_list = get_spot_df()
df_bingx_list['binance_symbol'] = df_bingx_list['symbol'].apply(lambda x: x.replace('-', ''))
df_bingx_list['binance_btc_symbol'] = df_bingx_list['symbol'].apply(lambda x: x.split('-')[0] + 'BTC')
df_joined = df_bingx_list[df_bingx_list['binance_symbol'].isin(df_binance_symbols)]
sample_symbol = df_joined.loc[49:50]

binance_symbol_url = f"https://api.binance.com/api/v3/klines?symbol={sample_symbol.at[0, 'binance_symbol']}&interval=4h"
binance_symbol_data = requests.get(binance_symbol_url, headers=headers).json()
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
df_binance_symbol = pd.DataFrame(binance_symbol_data)
df_binance_symbol.columns = columns
df_binance_symbol['symbol'] = sample_symbol.at[0, 'binance_symbol']
df_binance_symbol['candlestick_chart_close_time'] = df_binance_symbol['candlestick_chart_close_time'].apply(
    convertToTimeStamp)
df_binance_symbol['candlestick_chart_open_time'] = df_binance_symbol['candlestick_chart_open_time'].apply(
    convertToTimeStamp)
df_binance_symbol = df_binance_symbol.set_index('candlestick_chart_close_time').sort_index(ascending=True)
# %%
binance_symbol_url_btc = f"https://api.binance.com/api/v3/klines?symbol={sample_symbol.at[0, 'binance_btc_symbol']}&interval=4h"
binance_symbol_data_btc = requests.get(binance_symbol_url, headers=headers).json()
df_binance_symbol_btc = pd.DataFrame(binance_symbol_data_btc)
df_binance_symbol_btc.columns = columns
df_binance_symbol_btc['symbol'] = sample_symbol.at[0, 'binance_btc_symbol']
df_binance_symbol_btc['candlestick_chart_close_time'] = df_binance_symbol_btc['candlestick_chart_close_time'].apply(
    convertToTimeStamp)
df_binance_symbol_btc['candlestick_chart_open_time'] = df_binance_symbol_btc['candlestick_chart_open_time'].apply(
    convertToTimeStamp)
df_binance_symbol_btc = df_binance_symbol_btc.set_index('candlestick_chart_close_time').sort_index(ascending=True)
# %%
layout = go.Layout(autosize=True)
candlestick = go.Candlestick(
    x=df_binance_symbol.index,
    open=df_binance_symbol['open'],
    high=df_binance_symbol['high'],
    low=df_binance_symbol['low'],
    close=df_binance_symbol['close']
)
candlestick_btc = go.Candlestick(
    x=df_binance_symbol_btc.index,
    open=df_binance_symbol_btc['open'],
    high=df_binance_symbol_btc['high'],
    low=df_binance_symbol_btc['low'],
    close=df_binance_symbol_btc['close']
)

fig = go.Figure(data=[
    candlestick,
    candlestick_btc
],
    # layout=layout,
)
fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")

path = "test_all.png"
fig.write_image(path, width=1920, height=1080)
