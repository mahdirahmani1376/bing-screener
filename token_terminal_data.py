import requests
import pandas as pd
from tqdm import tqdm
from bingx_spot_list import get_spot_df
from datetime import datetime
from coin_market_cap import get_coin_market_cap_df

# cookies are important
cookies = {
    '_fbp': 'fb.1.1697708758055.1704677972',
    '_gcl_au': '1.1.1151732405.1697708760',
    'intercom-id-p3bihfmm': 'bed9ce03-c09b-408d-9589-fb15abedf4bc',
    'intercom-device-id-p3bihfmm': 'b6a13925-5e1b-4abb-89f9-226ef0cdcad9',
    '__stripe_mid': 'be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265',
    '_ga': 'GA1.1.1353671698.1697708757',
    'session': '74a93832-bfeb-415a-90ed-b892f80b5810',
    '_loggedin': '1',
    '_ga_TJ9TEYJ3GF': 'GS1.1.1702813667.22.1.1702814056.0.0.0',
    '__stripe_sid': 'ff45fea7-833e-48de-a94b-96c8026bc118562793',
    'intercom-session-p3bihfmm': 'OWhVVnpHdkhINGxENW4zaDdST245aFhYblI3aVU4bTVVUEZNY0pyd0xub2laclFvRmxDTGQ5YktBMEk2ZDZBSC0tMThtZGp1YjZkRndFVXBFZTVaOHY4dz09--88d6a65163f78a55ef126b5e1825084eb542d3d8',
    'ph_phc_amGyrGA1TpwJYYk2zNff9qfQkFBzu4uFghOgP6DjqIj_posthog': '%7B%22distinct_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24device_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1702814170381%2C%22018c779a-92a5-7974-b182-32dafad81a79%22%2C1702813668005%5D%2C%22%24client_session_props%22%3A%7B%22sessionId%22%3A%22018c779a-92a5-7974-b182-32dafad81a79%22%2C%22props%22%3A%7B%22initialPathName%22%3A%22%2Fterminal%2Fdatasets%2Fcrypto-screener%22%2C%22referringDomain%22%3A%22%24direct%22%7D%7D%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Atrue%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%2C%22%24session_recording_network_payload_capture%22%3A%7B%22capturePerformance%22%3Afalse%7D%2C%22%24stored_person_properties%22%3A%7B%22tt_tier%22%3A%22free%22%7D%7D',
}

headers = {
    'authority': 'tokenterminal.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    # 'cookie': '_fbp=fb.1.1697708758055.1704677972; _gcl_au=1.1.1151732405.1697708760; intercom-id-p3bihfmm=bed9ce03-c09b-408d-9589-fb15abedf4bc; intercom-device-id-p3bihfmm=b6a13925-5e1b-4abb-89f9-226ef0cdcad9; __stripe_mid=be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265; _ga=GA1.1.1353671698.1697708757; session=74a93832-bfeb-415a-90ed-b892f80b5810; _loggedin=1; _ga_TJ9TEYJ3GF=GS1.1.1702813667.22.1.1702814056.0.0.0; __stripe_sid=ff45fea7-833e-48de-a94b-96c8026bc118562793; intercom-session-p3bihfmm=OWhVVnpHdkhINGxENW4zaDdST245aFhYblI3aVU4bTVVUEZNY0pyd0xub2laclFvRmxDTGQ5YktBMEk2ZDZBSC0tMThtZGp1YjZkRndFVXBFZTVaOHY4dz09--88d6a65163f78a55ef126b5e1825084eb542d3d8; ph_phc_amGyrGA1TpwJYYk2zNff9qfQkFBzu4uFghOgP6DjqIj_posthog=%7B%22distinct_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24device_id%22%3A%22018b8f9d-82d0-7998-a9be-72eb8c3bad4f%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1702814170381%2C%22018c779a-92a5-7974-b182-32dafad81a79%22%2C1702813668005%5D%2C%22%24client_session_props%22%3A%7B%22sessionId%22%3A%22018c779a-92a5-7974-b182-32dafad81a79%22%2C%22props%22%3A%7B%22initialPathName%22%3A%22%2Fterminal%2Fdatasets%2Fcrypto-screener%22%2C%22referringDomain%22%3A%22%24direct%22%7D%7D%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Atrue%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%2C%22%24session_recording_network_payload_capture%22%3A%7B%22capturePerformance%22%3Afalse%7D%2C%22%24stored_person_properties%22%3A%7B%22tt_tier%22%3A%22free%22%7D%7D',
    'if-none-match': 'W/"49ec7b892e405e13e893a8a868646098"',
    'purpose': 'prefetch',
    'referer': 'https://tokenterminal.com/terminal/datasets/crypto-screener',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-nextjs-data': '1',
}

df_list = []
for i in tqdm(range(0, 3)):
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
# %%
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
    # "tvl_30d_trend",
    "tvl_30d_change",
    "tvl_90d_avg",
    "tvl_90d_change",
    "tvl_180d_avg",
    "tvl_180d_change",
    "tvl_365d_avg",
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
    "trading_volume_7d_sum",
    "trading_volume_30d_sum",
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
    "quote.USD.fully_diluted_market_cap",
    "volume_mcap",
    "platform.symbol",
    "tvl_ratio",
    "cmc_rank"
]
df_token_terminal = pd.DataFrame()
for i in df_list:
    df_token_terminal = pd.concat([df_token_terminal, i])

df_coin_market_cap = get_coin_market_cap_df()
df_joined = pd.merge(df_token_terminal, df_coin_market_cap, how='left', left_on='project_dbt_tag', right_on='slug')

df_result = df_joined[columns]
df_result['pf_filter'] = (df_result['pf_fully_diluted_7d_change'] < df_result['pf_fully_diluted_30d_change']) \
                         & (df_result['pf_fully_diluted_30d_change'] < df_result['pf_fully_diluted_90d_change']) \
                         & (df_result['pf_fully_diluted_90d_change'] < df_result['pf_fully_diluted_180d_change'])

df_result['tvl_filter'] = (df_result['tvl_7d_change'] > df_result['tvl_30d_change']) \
                          & (df_result['tvl_30d_change'] > df_result['tvl_90d_change']) \
                          & (df_result['tvl_90d_change'] > df_result['tvl_180d_change'])

df_result['tvl_to_mcap_7d'] = df_result['tvl_7d_avg'] / df_result['market_cap_fully_diluted_max_latest']
df_result['tvl_to_mcap_30d'] = df_result['tvl_30d_avg'] / df_result['market_cap_fully_diluted_max_latest']
df_result['trading_vol_7d_mcap'] = df_result['token_trading_volume_7d_sum'] / df_result[
    'market_cap_fully_diluted_max_latest']
df_result['trading_vol_30d_mcap'] = df_result['token_trading_volume_30d_sum'] / df_result[
    'market_cap_fully_diluted_max_latest']
df_result['deposit_mcap_7d'] = df_result['net_deposits_7d_avg'] / df_result['market_cap_fully_diluted_max_latest']
df_result['deposit_mcap_30d'] = df_result['net_deposits_30d_avg'] / df_result['market_cap_fully_diluted_max_latest']

df_result['price_30d_change'] = df_result['price_30d_change'] * 100
df_result['price_7d_change'] = df_result['price_7d_change'] * 100
df_result['price_24h_change'] = df_result['price_24h_change'] * 100

with pd.ExcelWriter(f'data/token_terminal-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx') as writer:
    df_result.to_excel(writer)

# with pd.ExcelWriter(f'data/token_terminal-all-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx') as writer:
#     df_token_terminal.to_excel(writer)
# df_coin_market_cap = get_coin_market_cap_df()
# df_joined = pd.merge(df_token_terminal, df_coin_market_cap,how= 'left', left_on='project_dbt_tag', right_on='slug')
# with pd.ExcelWriter(f'data/token_terminal-all-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx') as writer:
#     df_joined.to_excel(writer)
