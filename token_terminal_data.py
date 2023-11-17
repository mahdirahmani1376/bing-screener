import requests
import pandas as pd
from tqdm import tqdm
from bingx_spot_list import get_spot_df
from datetime import datetime
# cookies are important
cookies = {
    '_fbp': 'fb.1.1697708758055.1704677972',
    '_gcl_au': '1.1.1151732405.1697708760',
    'intercom-id-p3bihfmm': 'bed9ce03-c09b-408d-9589-fb15abedf4bc',
    'intercom-device-id-p3bihfmm': 'b6a13925-5e1b-4abb-89f9-226ef0cdcad9',
    '__stripe_mid': 'be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265',
    'session': 'b312073b-9da1-4230-91fa-c407c2771140',
    '_ga': 'GA1.1.1353671698.1697708757',
    'intercom-session-p3bihfmm': '',
    'ph_phc_amGyrGA1TpwJYYk2zNff9qfQkFBzu4uFghOgP6DjqIj_posthog': '%7B%22distinct_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24device_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1699625507213%2C%22018bb993-198d-705e-b506-efb1d3eab032%22%2C1699625507213%5D%2C%22%24client_session_props%22%3A%7B%22sessionId%22%3A%22018bb993-198d-705e-b506-efb1d3eab032%22%2C%22props%22%3A%7B%22initialPathName%22%3A%22%2Fterminal%2Fcrypto-screener%22%2C%22referringDomain%22%3A%22%24direct%22%7D%7D%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Atrue%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%7D',
    '__stripe_sid': '64f9f93c-bc8b-40e5-9abb-82080de54cce36442c',
    '_ga_TJ9TEYJ3GF': 'GS1.1.1700214255.18.1.1700214301.0.0.0',
}

headers = {
    'x-tt-terminal-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcm9udEVuZCI6InRlcm1pbmFsIGRhc2hib2FyZCIsImlhdCI6MTcwMDE4MDUwOCwiZXhwIjoxNzAxMzkwMTA4fQ.W0K1Vr27UC5xprjeARrCEHgT5KAnh33LO52mqNnXihI',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Referer': 'https://tokenterminal.com/',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'Bearer c0e5035a-64f6-4d2c-b5f6-ac1d1cb3da2f',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
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
# "price_90d_change",
# "price_180d_trend",
# "price_365d_trend",
# "market_cap_fully_diluted_max_latest",
# "market_cap_circulating_max_latest",
# "token_trading_volume_24h_sum",
# "token_trading_volume_24h_change",
# "token_trading_volume_7d_sum",
# "token_trading_volume_7d_change",
# "token_trading_volume_30d_sum",
# "token_trading_volume_30d_change",
# "net_deposits_7d_avg",
# "net_deposits_30d_avg",
# "net_deposits_90d_avg",
# "tvl_24h_avg",
"tvl_24h_change",
# "tvl_7d_avg",
"tvl_7d_change",
# "tvl_30d_avg",
# "tvl_30d_trend",
"tvl_30d_change",
# "tvl_90d_avg",
"tvl_90d_change",
# "tvl_180d_avg",
"tvl_180d_change",
# "tvl_365d_avg",
"tvl_365d_change",
# "tvl_max_ath",
# "tvl_max_atl",
# "transaction_volume_24h_avg",
# "transaction_volume_24h_change",
# "transaction_volume_7d_avg",
# "transaction_volume_7d_change",
# "transaction_volume_30d_avg",
# "transaction_volume_30d_change",
# "trading_volume_24h_sum",
# "trading_volume_7d_sum",
# "trading_volume_30d_sum",
"pf_fully_diluted_24h_change",
"pf_fully_diluted_7d_change",
"pf_fully_diluted_30d_change",
"pf_fully_diluted_90d_change",
"pf_fully_diluted_180d_change",
"pf_fully_diluted_365d_change",
# "pf_fully_diluted_24h_trend",
# "pf_fully_diluted_7d_trend",
# "pf_fully_diluted_30d_trend",
# "pf_fully_diluted_90d_trend",
# "pf_fully_diluted_180d_trend",
# "pf_fully_diluted_365d_trend",
# "ps_fully_diluted_7d_change",
# "ps_fully_diluted_30d_change",
# "ps_fully_diluted_90d_change",
# "ps_fully_diluted_180d_change",
# "ps_fully_diluted_365d_change",
"market_cap_fully_diluted_max_latest",
]
df_token_terminal = pd.DataFrame()
for i in df_list:
    df_token_terminal = pd.concat([df_token_terminal,i])
df_token_terminal = df_token_terminal[columns]
with pd.ExcelWriter(f'data/token_terminal-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx') as writer:
    df_token_terminal.to_excel(writer)
