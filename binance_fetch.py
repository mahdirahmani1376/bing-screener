import requests
import pandas as pd
from bingx_spot_list import get_spot_df

url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}
symbols_url = 'https://api.binance.com/api/v3/exchangeInfo'

response_binance_list = requests.get(symbols_url,headers=headers).json()
#%%
df_binance_symbols = pd.DataFrame(response_binance_list['symbols'])['symbol'].values.tolist()
#%%
df_bingx_list = get_spot_df()
#%%
df_bingx_list['binance_symbol'] = df_bingx_list['symbol'].apply(lambda x: x.replace('-', ''))
#%%
df_joined = df_bingx_list[df_bingx_list['binance_symbol'].isin(df_binance_symbols)]
#%%
sample_symbol = df_joined.iloc[0:1]
#%%
binance_symbol_url = f"https://api.binance.com/api/v3/klines?symbol={sample_symbol.at[0,'binance_symbol']}&interval=4h"
binance_symbol_data = requests.get(binance_symbol_url,headers=headers).json()
