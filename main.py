import requests
import pandas as pd
from requests import Request, Session


cookies = {
    'cookieControl': 'true',
    'cookieControlPrefs': '%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D',
    'PHPSESSID': 'cbb9ff96887882a408c4f26662a7a596',
}

headers = {
    'authority': 'www.cryptometer.io',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    # 'cookie': 'cookieControl=true; cookieControlPrefs=%5B%22preferences%22%2C%22analytics%22%2C%22marketing%22%5D; PHPSESSID=cbb9ff96887882a408c4f26662a7a596',
    'referer': 'https://www.cryptometer.io/volume-flow',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'req': 'volume_flow',
    'token': 'fab13e2dc7a0ccca50d1a9ff1f9dbe39efbdbab0db1682240592976d09d85050',
    'timeframe': 'd',
}

response = requests.get('https://www.cryptometer.io/ajaxToken.php', params=params, cookies=cookies, headers=headers)
#%%
jsonResponse = response.json()
dfFlowBuy = pd.DataFrame(jsonResponse['flow_buy'])
dfFlowSell = pd.DataFrame(jsonResponse['flow_sell'])
dfFlowNetVol = pd.DataFrame(jsonResponse['flow_net_vol'])
#%%
dfFlowBuyAggregate = dfFlowBuy[[1,2]].groupby(1).sum()
dfFlowBuyAggregate.rename(columns={2:'buyFlow'},inplace=True)

dfFlowSellAggregate = dfFlowSell[[0,2]].groupby(0).sum()
dfFlowSellAggregate.rename(columns={2:'sellFlow'},inplace=True)

dfFlowNetAggregate = dfFlowNetVol[[1,2]].groupby(1).sum()
dfFlowNetAggregate.rename(columns={2:'netFlow'},inplace=True)
dfAggregate = pd.concat([dfFlowBuyAggregate,dfFlowSellAggregate,dfFlowNetAggregate],axis=1)
#%%
CoinMarketCapKey = ''
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': CoinMarketCapKey,
}

session = Session()
session.headers.update(headers)
responseCoinMarketCap = session.get(url, params=parameters)
#%%
test = responseCoinMarketCap.json()
dfCoinMarketCap = pd.json_normalize(responseCoinMarketCap.json()['data'])
dfCoinMarketCap = dfCoinMarketCap[dfCoinMarketCap['cmc_rank'] < 500]
dfCoinMarketCap.set_index('symbol',inplace=True)
dfCoinMarketCap['volume_mackap'] =  dfCoinMarketCap['quote.USD.volume_24h'] / dfCoinMarketCap['quote.USD.market_cap']
# dfJoined = pd.DataFrame.merge(dfCoinMarketCap,dfAggregate)
dfJoined = dfCoinMarketCap.join(dfAggregate)
dfJoined['inflow_volume'] = dfJoined['buyFlow'] / dfJoined['quote.USD.volume_24h']
dfJoined['outflow_volume'] = dfJoined['sellFlow'] / dfJoined['quote.USD.volume_24h']
dfJoined['netflow_volume'] = dfJoined['netFlow'] / dfJoined['quote.USD.volume_24h']

dfJoinedPath = r"C:\Users\acer\Desktop\dfJoined.xlsx"
dfCoinMarketCapPath = r"C:\Users\acer\Desktop\dfCoinMarketCap.xlsx"
writerJoined = pd.ExcelWriter(path=dfJoinedPath)
writerCoinMarketCap = pd.ExcelWriter(path=dfCoinMarketCapPath)
with writerJoined as writer:
    dfJoined.to_excel(writer)
with writerCoinMarketCap as writer:
    dfCoinMarketCap.to_excel(writer)