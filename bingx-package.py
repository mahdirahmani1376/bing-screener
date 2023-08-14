from bingX.spot import Spot
import pandas as pd
import json


client = Spot(APIKEY, SECRETKEY)

currencyData = pd.DataFrame(client.symbols('BTC-USDT'))