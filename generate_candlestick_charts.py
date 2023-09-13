from glob import glob
import os
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm

from bingx import saveCandleStickChart,strongCloseCandle,strongCandle,showCandleStickChart,strongBody,strongBullishCandle,strongBerishCandle
from bingx import strongBearishSignal,strongBullishSignal,strongBullishSignalBar,bullishCloseAbovePastBars,openBelowLastDayClose,strongRatio

h4_time_frame = "4h"
h1_time_frame = "1h"
d1_time_frame = "1d"
time_frame = h4_time_frame

currencies = glob(f"data/{time_frame}/*.xlsx")
charts = glob(f"charts/{time_frame}/**/*.png",recursive=True)
charts = [os.path.join(os.path.dirname(__file__),i) for i in charts]
for i in charts:
    if os.path.isfile(i):
        os.remove(i)



for i in tqdm(currencies):
    try:
        filepath = os.path.join(os.path.dirname(__file__),i)
        df = pd.read_excel(filepath)
        # df = pd.read_excel("data//UNFI-USDT.xlsx")
        # df = pd.read_excel("data//WIFI-USDT.xlsx")
        # df = pd.read_excel("data//4h//MULTI-USDT.xlsx")

        df.set_index('candlestick_chart_close_time',inplace=True)

        df['last_day_high'] = df['high'].shift(periods=-1)
        df['last_day_low'] = df['low'].shift(periods=-1)

        df['strong_close'] = df.apply(strongCloseCandle,axis=1)
        df['strong_body'] = df.apply(strongBody,axis=1)
        df['strong'] = df.apply(strongCandle,axis=1)
        df['strong_bullish_signal'] = df.apply(strongBullishSignal,axis=1)
        df['strong_bearish_signal'] = df.apply(strongBearishSignal,axis=1)
        df['strong_bullish_signal_bar'] = df.apply(strongBullishSignalBar,axis=1)
        df['open_below_last_day_close'] = df.apply(openBelowLastDayClose,axis=1)
        df['strong_ratio'] = df.apply(strongRatio, axis=1)

        strongBullishCloseList = []
        strongBearishCloseList = []
        for index, value in enumerate(df['close']):
            bullishValueToAppend = value > df.iloc[index+1:index+20]['close'].max()
            bearishValueToAppend = value < df.iloc[index+1:index+20]['close'].min()
            strongBullishCloseList.append(bullishValueToAppend)
            strongBearishCloseList.append(bearishValueToAppend)

        df['strong_bullish_close_past_bars_before'] = strongBullishCloseList
        df['strong_bearish_close_past_bars_before'] = strongBearishCloseList

        dfFinal = df.iloc[1:2]
        # dfFinal = df
        if (True in dfFinal['strong_bullish_signal'].values or True in dfFinal['strong_ratio'].values) and (True in dfFinal['strong_bullish_close_past_bars_before'].values):
            savePathBullish = f"charts/{time_frame}/bullish"
            if not os.path.exists(savePathBullish):
                os.makedirs(savePathBullish)

            path = os.path.join(savePathBullish,f"{dfFinal['symbol'].values[0]}.png")
            saveCandleStickChart(df,path)
        if (True in dfFinal['strong_bearish_signal'].values or True in dfFinal['strong_ratio'].values) and (True in dfFinal['strong_bearish_close_past_bars_before'].values):
            savePathBearish = f"charts/{time_frame}/bearish"
            if not os.path.exists(savePathBearish):
                os.makedirs(savePathBearish)

            path = os.path.join(savePathBearish,f"{dfFinal['symbol'].values[0]}.png")
            saveCandleStickChart(df,path)
    except Exception as e:
        print(filepath)
        print(e)

