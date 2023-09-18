import pandas as pd
import requests
def get_crypto_meter_dataframe():
    cookies = {
        'cookieControl': 'true',
        'cookieControlPrefs': '%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D',
        '__gads': 'ID=1213e9598e6dbafa:T=1671607514:S=ALNI_Mbyse-h16WjM-9LMv17A0D4TxqIdg',
        '__gpi': 'UID=00000b95a50719b8:T=1671607514:RT=1671607514:S=ALNI_MamwSzR590dczzjUMRCHhpxsIPJYQ',
        'cto_bundle': 'DFRgfl9yWEV6N0ZCaU5LNkFveSUyQkpPT05qJTJCRm1VVDltTlhoWHdrRnFUOGRvJTJGRlpMamJXZEolMkY1SUlINktFS2I1QWhUandjZktqYjR0NmJWNlA4ZXc4OCUyQndvTjBUcXJFc0x6bnZHRXZXSllXUWpVWW5IbUtlZXNoWTk1TnBaMUtUMnlLdHdtcElIdFZ3ZVo0V2RScHFRU0hkSDdBJTNEJTNE',
        'xa_sessid': '15d2a35574f520f5489f60fdd76a2cff',
        'xa_valid': 'cc47247239c6c1222afd2fef705d3406e7452792e49e1c7792e1dcb3d4b2f635',
        '_ga_43ZTZFMP3D': 'GS1.1.1694962363.1.0.1694962364.0.0.0',
        'twk_uuid_61820a016885f60a50ba1014': '%7B%22uuid%22%3A%221.7xY5XEjYvB4YiSDOJzdMyXnYLWvtIdThVsSnQjzna5qPTvqQX4KGw84L4SM5IIaubxchTG8aTqbxdOZbG1eDXAXTk5QPxSB3WjlqyU7cc6TCRIqNhKbwZA71%22%2C%22version%22%3A3%2C%22domain%22%3A%22cryptometer.io%22%2C%22ts%22%3A1694962365759%7D',
        '_gid': 'GA1.2.1076995558.1694962368',
        'PHPSESSID': '0526a0c521dbae272e625c78ef13912e',
        '_ga': 'GA1.1.865946597.1671607478',
        '_ga_9ZT12HEGGM': 'GS1.1.1695036724.5.1.1695036729.55.0.0',
    }

    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    params = {
        'req': 'volume_flow_table_view',
        'token': '4c150ea2726502ced17b846158309423cc48e3b9b7510ffc8296edfbabcb3928',
        'filter': 'all',
        'timeframe': 'd',
        '_': '1694962103356',
    }

    response = requests.get('https://www.cryptometer.io/ajaxToken.php', params=params, cookies=cookies, headers=headers)
    data = response.json()['data']
    df = pd.DataFrame(data)
    df.dropna(subset='mcap_raw',inplace=True)
    df.dropna(subset='inflow_raw',inplace=True)
    df['inflow_raw'] = df['inflow_raw'].astype(float)
    df['mcap_raw'] = df['mcap_raw'].astype(float)
    df = df[df['mcap_raw'] > 0]
    df['volume_mcap'] = df['inflow_raw'] / df['mcap_raw']
    df = df.sort_values('volume_mcap',ascending=False)
    df['name'] = df['name'].apply(lambda x: str(x) + '-USDT')

    return df

