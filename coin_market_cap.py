import pandas as pd
import requests
import json

with open('credentials.json') as file:
    jsonFile = json.load(file)
    X_CMC_PRO_API_KEY = jsonFile['X-CMC_PRO_API_KEY']


def get_coin_market_cap_df():
    headers = {
        "X-CMC_PRO_API_KEY": X_CMC_PRO_API_KEY
    }
    response = requests.get(
        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD',
        headers=headers).json()
    df = pd.json_normalize(response['data'])
    df = df[df['quote.USD.market_cap'] > 0]
    df['volume_mcap'] = df["quote.USD.volume_24h"] / df["quote.USD.market_cap"]
    df.sort_values(by=['volume_mcap'], ascending=False, inplace=True)
    df['symbol'] = df['symbol'].apply(lambda x: str(x) + '-USDT')
    return df

def get_info_for_url(url):
    headers = {
        "X-CMC_PRO_API_KEY": X_CMC_PRO_API_KEY
    }
    response = requests.get(
        url,
        headers=headers).json()
    df = pd.json_normalize(response['data'])
    df = df[df['quote.USD.market_cap'] > 0]
    df['volume_mcap'] = df["quote.USD.volume_24h"] / df["quote.USD.market_cap"]
    df.sort_values(by=['volume_mcap'], ascending=False, inplace=True)
    df['symbol'] = df['symbol'].apply(lambda x: str(x) + '-USDT')
    return df