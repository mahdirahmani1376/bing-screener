import pandas as pd
import requests
from coin_market_cap import get_coin_market_cap_df

def get_crypto_meter_dataframe():
    cookies = {
        '_ga': 'GA1.1.928168899.1703515594',
        'cookieControl': 'true',
        'cookieControlPrefs': '%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D',
        'PHPSESSID': 'c0ecf1f3fdfd8ddc1804ef55ac86d197',
        '_ga_9ZT12HEGGM': 'GS1.1.1703592373.3.1.1703593518.60.0.0',
    }

    headers = {
        'authority': 'www.cryptometer.io',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
        # 'cookie': '_ga=GA1.1.928168899.1703515594; cookieControl=true; cookieControlPrefs=%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D; PHPSESSID=c0ecf1f3fdfd8ddc1804ef55ac86d197; _ga_9ZT12HEGGM=GS1.1.1703592373.3.1.1703593518.60.0.0',
        'referer': 'https://www.cryptometer.io/volume-flow?v=table-view',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'req': 'volume_flow_table_view',
        'token': '71b3486fa12b406c600aa1423b3d49949c859a5b42b9eaeeddfd80493c82c4d0',
        'filter': 'all',
        'timeframe': 'd',
        '_': '1703593518938',
    }

    response = requests.get('https://www.cryptometer.io/ajaxToken.php', params=params, cookies=cookies, headers=headers)
    data = response.json()['data']
    df = pd.DataFrame(data)
    df.dropna(subset='mcap_raw',inplace=True)
    df.dropna(subset='inflow_raw',inplace=True)
    df['inflow_raw'] = df['inflow_raw'].astype(float)
    df['mcap_raw'] = df['mcap_raw'].astype(float)
    df = df[df['mcap_raw'] > 0]
    # df['volume_mcap'] = df['inflow_raw'] / df['mcap_raw']
    df['outflow_mcap'] = df['outflow_raw'] / df['mcap_raw']
    df['inflow_mcap'] = df['inflow_raw'] / df['mcap_raw']
    # df = df.sort_values('volume_mcap',ascending=False)
    df = df.sort_values('outflow_mcap',ascending=False)
    df['name'] = df['name'].apply(lambda x: str(x) + '-USDT')

    return df

if (__name__ == '__main__'):
    df = get_crypto_meter_dataframe()
    df_coin_market_cap = get_coin_market_cap_df()
    df_coin_market_cap_500 = df_coin_market_cap[df_coin_market_cap['cmc_rank'] < 501]
    df_joined = pd.merge(df,df_coin_market_cap_500,'inner',left_on='name',right_on='symbol')
    df_joined['outflow_vol'] = df_joined['outflow_raw'] / df_joined['quote.USD.volume_24h']
    df_joined['inflow_vol'] = df_joined['inflow_raw'] / df_joined['quote.USD.volume_24h']
    with pd.ExcelWriter('crypto_meter.xlsx') as writer:
        df_joined.to_excel(writer)
