from glob import glob
import os
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm

from bingx import saveCandleStickChart,strongCloseCandle,strongCandle,showCandleStickChart,strongBody,strongBullishCandle,strongBerishCandle
from bingx import strongBearishSignal,strongBullishSignal

currencies = glob('data/*.xlsx')

for i in tqdm(currencies):
    try:
        filepath = os.path.join(os.path.dirname(__file__),i)
        df = pd.read_excel(filepath)
        df.set_index('candlestick_chart_close_time',inplace=True)
        df['strong_close'] = df.apply(strongCloseCandle,axis=1)
        df['strong_body'] = df.apply(strongBody,axis=1)
        df['strong'] = df.apply(strongCandle,axis=1)
        df['strong_bullish_signal'] = df.apply(strongBullishSignal,axis=1)
        df['strong_bearish_signal'] = df.apply(strongBearishSignal,axis=1)
        dfFinal = df.iloc[1:2]
        if True in dfFinal['strong_bullish_signal'].values:
            path = f"charts/bullish/{dfFinal['symbol'].values[0]}.png"
            saveCandleStickChart(df,path)
        if True in dfFinal['strong_bearish_signal'].values:
            path = f"charts/bearish/{dfFinal['symbol'].values[0]}.png"
            saveCandleStickChart(df,path)
    except Exception as e:
        print(e)

