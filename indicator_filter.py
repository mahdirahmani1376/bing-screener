import pandas_ta as ta
import pandas as pd

def adx_signal(row):
    if (row['DMP_14'] > row['DMN_14']) and (row['ADX_14'] > 20):
        return 1
    elif (row['DMN_14'] > row['DMP_14']) and (row['ADX_14'] > 20):
        return -1
    else:
        return 0

# df = pd.read_excel("data//4h//PERP-USDT.xlsx")
# df.set_index('candlestick_chart_close_time', inplace=True)
# df.sort_index(inplace=True,ascending=True)
# df_adx = df.ta.adx(high=df['high'],low= df['low'],close= df['close'], length = 14)
# df_merged = pd.concat([df,df_adx],axis=1,join='inner')
# df_merged['adx_rating'] = df_merged.apply(adx_signal,axis=1)

# df_ma = ta.ema(ta.ohlc4(df["open"], df["high"], df["low"], df["close"]), length=20)
# df_ma20 = ta.ema(ta.ohlc4(df["open"], df["high"], df["low"], df["close"]), length=20)

