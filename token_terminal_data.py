import requests
import pandas as pd

cookies = {
    '_gid': 'GA1.2.1569656627.1697708758',
    '_fbp': 'fb.1.1697708758055.1704677972',
    '_gcl_au': '1.1.1151732405.1697708760',
    'intercom-id-p3bihfmm': 'bed9ce03-c09b-408d-9589-fb15abedf4bc',
    'intercom-session-p3bihfmm': '',
    'intercom-device-id-p3bihfmm': 'b6a13925-5e1b-4abb-89f9-226ef0cdcad9',
    '__stripe_mid': 'be998070-b8ce-49f7-a7b4-cde46e5fe1a29b1265',
    '__stripe_sid': '73bc035c-e0cd-41b9-bd0d-778d180a5c0ddfb2eb',
    'session': '20e25f11-762e-436e-b3af-616c3773402c',
    '_loggedin': '1',
    '_ga': 'GA1.1.1353671698.1697708757',
    '_ga_TJ9TEYJ3GF': 'GS1.1.1697713950.3.1.1697713999.0.0.0',
}

headers = {
    'authority': 'api.tokenterminal.com',
    'accept': 'application/json',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://tokenterminal.com',
    'referer': 'https://tokenterminal.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-tt-terminal-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcm9udEVuZCI6InRlcm1pbmFsIGRhc2hib2FyZCIsImlhdCI6MTY5NzY3NDg0MiwiZXhwIjoxNjk4ODg0NDQyfQ.sSaeEi94WIc0MHT34EMyz9VdFPvL444YKL73NmC0ibU',
}

json_data = {
    'startRow': 100,
    'endRow': 200,
    'rowGroupCols': [],
    'valueCols': [],
    'pivotCols': [],
    'pivotMode': False,
    'groupKeys': [],
    'filterModel': {},
    'sortModel': [
        {
            'sort': 'desc',
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
#%%
# with pd.ExcelWriter('data/token_terminal.xlsx') as writer:
#     df.to_excel(writer)