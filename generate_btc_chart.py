import pandas as pd
import requests

from bingx_spot_list import get_spot_df

usd_sample = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=[USD]',
btc_sample = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=[BTC]',
df_bingx = get_spot_df()

