import pandas as pd
import pandas_ta as ta




df = pd.read_excel("test.xlsx")
df.set_index(pd.DatetimeIndex(df["candlestick_chart_close_time"]), inplace=True)
# df.set_index('candlestick_chart_close_time', inplace=True)
df.sort_index(inplace=True, ascending=True)

if __name__ == '__main__':
    MyStrategy = ta.Strategy(
        name="DCSMA10",
        ta=[
            {"kind": "sma", "length": 10},
            {"kind": "sma", "length": 20},
            {"kind": "sma", "length": 30},
            {"kind": "ema", "length": 10},
            {"kind": "ema", "length": 20},
            {"kind": "ema", "length": 30},
            {"kind": "rsi"},
            {"kind": "macd"},
            {"kind": "vwma"},
            {"kind": "hma"},
            {"kind": "stoch"},
            {"kind": "cci"},
            {"kind": "ao"},
            {"kind": "mom"},
            {"kind": "stochrsi"},
            {"kind": "willr"},
            {"kind": "uo"},
            {"kind": "ichimoku"},
            {"kind": "adx"},
        ]
    )

    df.ta.strategy(MyStrategy)

    help(ta.ao)
    # help(ta.xsignals)
    # df.ta.strategy(verbose=True)
    # df.ta.strategy(timed=True)
    df.index.dtype