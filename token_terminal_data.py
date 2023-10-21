import requests
import pandas as pd
from tqdm import tqdm
from bingx_spot_list import get_spot_df
# cookies are important
cookies = {
    '_gid': 'GA1.2.1569656627.1697708758',
    '_fbp': 'fb.1.1697708758055.1704677972',
    '_gcl_au': '1.1.1151732405.1697708760',
    'intercom-id-p3bihfmm': 'bed9ce03-c09b-408d-9589-fb15abedf4bc',
    'intercom-session-p3bihfmm': '',
    'intercom-device-id-p3bihfmm': 'b6a13925-5e1b-4abb-89f9-226ef0cdcad9',
    '__stripe_mid': 'be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265',
    '_ga': 'GA1.2.1353671698.1697708757',
    '__stripe_sid': 'dc216c7a-6253-4ecc-8fbc-dc3b14cfac811c7785',
    '_gat_UA-136646465-3': '1',
    'session': 'b312073b-9da1-4230-91fa-c407c2771140',
    '_loggedin': '1',
    '_ga_TJ9TEYJ3GF': 'GS1.1.1697796594.7.1.1697796763.0.0.0',
}
cookies = {
    '_gid': 'GA1.2.1569656627.1697708758',
    '_fbp': 'fb.1.1697708758055.1704677972',
    '_gcl_au': '1.1.1151732405.1697708760',
    'intercom-id-p3bihfmm': 'bed9ce03-c09b-408d-9589-fb15abedf4bc',
    'intercom-session-p3bihfmm': '',
    'intercom-device-id-p3bihfmm': 'b6a13925-5e1b-4abb-89f9-226ef0cdcad9',
    '__stripe_mid': 'be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265',
    'session': 'b312073b-9da1-4230-91fa-c407c2771140',
    '_loggedin': '1',
    '_gat_UA-136646465-3': '1',
    '_ga': 'GA1.1.1353671698.1697708757',
    '_ga_TJ9TEYJ3GF': 'GS1.1.1697798912.8.1.1697798919.0.0.0',
}

headers = {
    'authority': 'api.tokenterminal.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    'if-none-match': 'W/"673da-euWskXPjbw2ZN9+yE30bzi4fu+U"',
    'origin': 'https://tokenterminal.com',
    'referer': 'https://tokenterminal.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-tt-terminal-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcm9udEVuZCI6InRlcm1pbmFsIGRhc2hib2FyZCIsImlhdCI6MTY5Nzc2MTIzMiwiZXhwIjoxNjk4OTcwODMyfQ.T__jKw6W62LVd6xa8Wf0qKp530vjoO_9xZVHAtNznJw',
}

df_list = []
for i in tqdm(range(0,3)):
    json_data = {
        'startRow': i * 100,
        'endRow': (i + 1) * 100,
        'rowGroupCols': [],
        'valueCols': [],
        'pivotCols': [],
        'pivotMode': False,
        'groupKeys': [],
        'filterModel': {},
        'sortModel': [
            {
                'sort': 'asc',
                'colId': 'tvl_7d_change',
            },
        ],
    }

    response = requests.post(
        'https://api.tokenterminal.com/v2/internal/marts/crypto_screener',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    json_response = response.json()
    df = pd.json_normalize(json_response['data'])
    df_list.append(df)
#%%
columns = [
"project_name",
"price_24h_change",
"price_7d_change",
"price_30d_change",
"price_90d_change",
"price_180d_trend",
"price_365d_trend",
"market_cap_fully_diluted_max_latest",
"market_cap_circulating_max_latest",
"token_trading_volume_24h_sum",
"token_trading_volume_24h_change",
"token_trading_volume_7d_sum",
"token_trading_volume_7d_change",
"token_trading_volume_30d_sum",
"token_trading_volume_30d_change",
"net_deposits_7d_avg",
"net_deposits_30d_avg",
"net_deposits_90d_avg",
"tvl_24h_avg",
"tvl_24h_change",
"tvl_7d_avg",
"tvl_7d_change",
"tvl_30d_avg",
"tvl_30d_trend",
"tvl_30d_change",
"tvl_90d_avg",
"tvl_90d_change",
"tvl_180d_avg",
"tvl_180d_change",
"tvl_365d_avg",
"tvl_365d_change",
"tvl_max_ath",
"tvl_max_atl",
"transaction_volume_24h_avg",
"transaction_volume_24h_change",
"transaction_volume_7d_avg",
"transaction_volume_7d_change",
"transaction_volume_30d_avg",
"transaction_volume_30d_change",
"trading_volume_24h_sum",
"trading_volume_7d_sum",
"trading_volume_30d_sum",
"pf_fully_diluted_24h_change",
"pf_fully_diluted_7d_change",
"pf_fully_diluted_30d_change",
"pf_fully_diluted_90d_change",
"pf_fully_diluted_180d_change",
"pf_fully_diluted_365d_change",
"ps_fully_diluted_7d_change",
"ps_fully_diluted_30d_change",
"ps_fully_diluted_90d_change",
"ps_fully_diluted_180d_change",
"ps_fully_diluted_365d_change",
"market_cap_fully_diluted_max_latest",
]
df_token_terminal = pd.DataFrame()
for i in df_list:
    df_token_terminal = pd.concat([df_token_terminal,i])
df_token_terminal = df_token_terminal[columns]
with pd.ExcelWriter('data/token_terminal.xlsx') as writer:
    df_token_terminal.to_excel(writer)
