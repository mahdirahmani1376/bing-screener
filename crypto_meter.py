import pandas as pd
import requests

cookies = {
    'cookieControl': 'true',
    'cookieControlPrefs': '%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D',
    '_ga': 'GA1.1.865946597.1671607478',
    '__gads': 'ID=1213e9598e6dbafa:T=1671607514:S=ALNI_Mbyse-h16WjM-9LMv17A0D4TxqIdg',
    '__gpi': 'UID=00000b95a50719b8:T=1671607514:RT=1671607514:S=ALNI_MamwSzR590dczzjUMRCHhpxsIPJYQ',
    'cto_bundle': 'DFRgfl9yWEV6N0ZCaU5LNkFveSUyQkpPT05qJTJCRm1VVDltTlhoWHdrRnFUOGRvJTJGRlpMamJXZEolMkY1SUlINktFS2I1QWhUandjZktqYjR0NmJWNlA4ZXc4OCUyQndvTjBUcXJFc0x6bnZHRXZXSllXUWpVWW5IbUtlZXNoWTk1TnBaMUtUMnlLdHdtcElIdFZ3ZVo0V2RScHFRU0hkSDdBJTNEJTNE',
    'PHPSESSID': '9f9a0ad7d21e519bcf097e2f3e9d9dd8',
    '_ga_9ZT12HEGGM': 'GS1.1.1694960328.3.1.1694962103.60.0.0',
}

headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

params = {
    'req': 'volume_flow_table_view',
    'token': '07c23562afacd576881827360fd545dc9d75d782892f9f3d415329dd343c5d3b',
    'filter': 'all',
    'timeframe': 'd',
    '_': '1694962103356',
}

response = requests.get('https://www.cryptometer.io/ajaxToken.php', params=params, cookies=cookies, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
df['n']
df.dropna(subset='mcap_raw',inplace=True)
df.dropna(subset='inflow_raw',inplace=True)
df['volume_mcap'] = df['inflow_raw'] / df['mcap_raw']
df = df.sort_values('volume_mcap')