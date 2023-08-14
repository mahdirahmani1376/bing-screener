import requests

cookies = {
    '__cfruid': '5b889fb53281546463e2e063d9a9f71c11dcbb7c-1691737426',
    '__cf_bm': 'a5ZYme5xjhLRe98tpKUwVFP3NM91No9cnYiUPg0kyNs-1691744994-0-AbBBtD7xpZ5vFj4nZxZtSLi+bg3lGM5XZJljqeImaUtiMRiYTpH+edef6PRdo1P1+X8NhW+8Xr+Z/E3BBOQzojw=',
}

headers = {
    'authority': 'api-app.qq-os.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    'app_version': '4.71.8',
    'appid': '30004',
    'channel': 'official',
    # 'cookie': '__cfruid=5b889fb53281546463e2e063d9a9f71c11dcbb7c-1691737426; __cf_bm=a5ZYme5xjhLRe98tpKUwVFP3NM91No9cnYiUPg0kyNs-1691744994-0-AbBBtD7xpZ5vFj4nZxZtSLi+bg3lGM5XZJljqeImaUtiMRiYTpH+edef6PRdo1P1+X8NhW+8Xr+Z/E3BBOQzojw=',
    'device_id': 'd5a05b08-df35-4b33-a7db-d857eea54a5c',
    'lang': 'en',
    'mainappid': '10009',
    'origin': 'https://bingx.com',
    'platformid': '30',
    'reg_channel': 'official',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sign': '9EA72F83D799CCBE865BFBE7ABDF3070A10B97DC011C39C8F5F14D30CE115B31',
    'timestamp': '1691745320995',
    'timezone': '3.5',
    'traceid': 'c9c1f52136714e71aba02d7a62f6fe9a',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'visitorid': '-1',
}

params = {
    'symbol': 'BTC_USDT',
    'bizType': '1',
    'period': '1day',
    'pagingSize': '301',
    'startTimestamp': '1691798400000',
    'timeZone': '8',
}

response = requests.get('https://api-app.qq-os.com/api/uni-market/v1/kline/list', params=params, cookies=cookies, headers=headers)