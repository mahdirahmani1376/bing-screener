from glob import glob
from bingx import *
import os
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm
from bingx_perpetual_list import get_perpetual_df
# from indicator_filter import adx_signal

# h4_time_frame = "4h"
# h1_time_frame = "1h"
# d1_time_frame = "1d"
# time_frame = h4_time_frame
how_many_candles_before = 2
volume_mcap = ""
filepath = ""

currencies = glob(f"data/{time_frame}/*.xlsx")
charts = glob(f"charts/{time_frame}/**/*.png", recursive=True)
charts = [os.path.join(os.path.dirname(__file__), i) for i in charts]
for i in charts:
    if os.path.isfile(i):
        os.remove(i)

df_perpetual = get_perpetual_df()
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

for i in tqdm(currencies):
    try:
        filepath = os.path.join(os.path.dirname(__file__), i)
        df = pd.read_excel(filepath)
        # df = pd.read_excel("data//ARK-USDT.xlsx")
        df.set_index('candlestick_chart_close_time', inplace=True)
        dfFinal = df.iloc[1:how_many_candles_before]

        if (
                (
                        True in dfFinal['atr_rating'].values
                        or True in dfFinal['strong_bullish_signal'].values
                        or True in dfFinal['strong_ratio'].values
                )
                and (True in dfFinal['strong_bullish_close_past_bars_before'].values)
                and (dfFinal['adx_rating'].values[0] > 0)
        ):
            savePathBullish = f"charts/{time_frame}/bullish/{now}"
            path = getSavePath(savePathBullish,dfFinal)
            saveCandleStickChart(df, path)

        if ((
                True in dfFinal['strong_bearish_signal'].values
                or True in dfFinal['atr_rating'].values
                or True in dfFinal['strong_ratio'].values
        )
                and (True in dfFinal['strong_bearish_close_past_bars_before'].values)
                and (dfFinal['adx_rating'].values[0] < 0)
        ):
            if dfFinal['symbol'].values[0] in df_perpetual['symbol'].values:
                savePathBearish = f"charts/{time_frame}/bearish/{now}"
                path = getSavePath(savePathBearish, dfFinal)
                saveCandleStickChart(df, path)
    except Exception as e:
        print(filepath)
        print(e)
