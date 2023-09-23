from glob import glob
from bingx import *
import os
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm
from bingx_perpetual_list import get_perpetual_df
from indicator_filter import adx_signal

# h4_time_frame = "4h"
# h1_time_frame = "1h"
# d1_time_frame = "1d"
# time_frame = h4_time_frame
how_many_candles_before = 6
volume_mcap = ""
filepath = ""

currencies = glob(f"data/{time_frame}/*.xlsx")
charts = glob(f"charts/{time_frame}/**/*.png", recursive=True)
charts = [os.path.join(os.path.dirname(__file__), i) for i in charts]
for i in charts:
    if os.path.isfile(i):
        os.remove(i)

df_perpetual = get_perpetual_df()

for i in tqdm(currencies):
    try:
        filepath = os.path.join(os.path.dirname(__file__), i)
        df = pd.read_excel(filepath)
        # df = pd.read_excel("data//ARK-USDT.xlsx")

        df.set_index('candlestick_chart_close_time', inplace=True)

        dfFinal = df.iloc[1:how_many_candles_before]

        crypto_meter_data = ""
        if with_crypto_meter:
            df_join = pd.read_excel('screener_data_h4.xlsx').set_index('candlestick_chart_close_time')
            volume_mcap = round(df_join[df_join['symbol'] == dfFinal['symbol'].values[0]]['volume_mcap'].values[0], 3)
            rank = df_join[df_join['symbol'] == dfFinal['symbol'].values[0]]['rank'].values[0]
            if pd.isna(volume_mcap):
                crypto_meter_data = f""
            else:
                crypto_meter_data = f"r_{int(rank)}_v_{volume_mcap}"

        volume_coin_mcap = ""
        volume_coin_mcap_series = df_coin_market_cap[df_coin_market_cap['symbol'] == dfFinal['symbol'].values[0]][
            'volume_mcap'].values
        if len(volume_coin_mcap_series) > 0:
            volume_coin_mcap = round(volume_coin_mcap_series[0], 3)
        if (
                (
                True in dfFinal['strong_bullish_signal'].values
                or True in dfFinal['strong_ratio'].values
                )
                and (True in dfFinal['strong_bullish_close_past_bars_before'].values)
                # and (dfFinal['adx_rating'].values[0] > 0)
        ):
            savePathBullish = f"charts/{time_frame}/bullish"
            if not os.path.exists(savePathBullish):
                os.makedirs(savePathBullish)

            path = os.path.join(savePathBullish,
                                f"{dfFinal['symbol'].values[0]}_cm_{crypto_meter_data}_cmc_{volume_coin_mcap}.png")
            saveCandleStickChart(df, path)

        if (    (
                True in dfFinal['strong_bearish_signal'].values
                or True in dfFinal['strong_ratio'].values
                )
                # and (True in dfFinal['strong_bearish_close_past_bars_before'].values)
                # and (dfFinal['adx_rating'].values[0] < 0)
        ):
            if dfFinal['symbol'].values[0] in df_perpetual['symbol'].values:
                savePathBearish = f"charts/{time_frame}/bearish"
                if not os.path.exists(savePathBearish):
                    os.makedirs(savePathBearish)

                path = os.path.join(savePathBearish, f"{dfFinal['symbol'].values[0]}_{volume_mcap}.png")
                saveCandleStickChart(df, path)

    except Exception as e:
        print(filepath)
        print(e)
