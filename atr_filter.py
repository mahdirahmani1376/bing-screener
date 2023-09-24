import pandas as pd
import pandas_ta as ta

df = pd.read_excel("test.xlsx")
# df.set_index(pd.DatetimeIndex(df["candlestick_chart_close_time"]), inplace=True)
df.set_index('candlestick_chart_close_time', inplace=True)
df.sort_index(inplace=True, ascending=True)

df_atr = df.ta.atr()
df = pd.concat([df, df_atr], axis=1, join='inner')
