import pandas as pd
import requests

def get_coin_market_cap_df():
    headers = {
        "X-CMC_PRO_API_KEY" : "8fefdde6-ba19-4941-9b99-32b4dbb500ca"
    }
    response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD',headers=headers).json()
    df = pd.json_normalize(response['data'])
    df = df[df['quote.USD.market_cap'] > 0]
    df['volume_mcap'] = df["quote.USD.volume_24h"] / df["quote.USD.market_cap"]
    df.sort_values(by=['volume_mcap'],ascending=False,inplace=True)
    df['symbol'] = df['symbol'].apply(lambda x: str(x) + '-USDT')
    return df
