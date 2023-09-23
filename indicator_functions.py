def adx_signal(row):
    try:
        if (row['DMP_14'] > row['DMN_14']) and (row['ADX_14'] > 20):
            return 1
        elif (row['DMN_14'] > row['DMP_14']) and (row['ADX_14'] > 20):
            return -1
        else:
            return 0
    except Exception as e:
        print(e)
        return 0

def atr_signal(row):
    try:
        return (row['close'] - row['open']) > (3 * row['ATRr_14'])
    except Exception as e:
        print(e)
        return 0

def sma_10(row):
    if (row['price'] > row['SMA_10']):
        return 1
    else:
        return -1
def sma_20(row):
    if (row['price'] > row['SMA_20']):
        return 1
    else:
        return -1
def sma_30(row):
    if (row['price'] > row['SMA_30']):
        return 1
    else:
        return -1

def ema_10(row):
    if (row['price'] > row['EMA_10']):
        return 1
    else:
        return -1

def ema_20(row):
    if (row['price'] > row['EMA_20']):
        return 1
    else:
        return -1

def ema_30(row):
    if (row['price'] > row['EMA_30']):
        return 1
    else:
        return -1
def rsi(row):
    if row['RSI_14'] < 30:
        return 1
    if row['RSI_14'] > 70:
        return -1
    else:
        return 0

def stochastic(row):
    if row['STOCHk_14_3_3'] > row['STOCHd_14_3_3'] and row['STOCHk_14_3_3'] < 20:
        return 1
    elif row['STOCHk_14_3_3'] < row['STOCHd_14_3_3'] and row['STOCHk_14_3_3'] > 80:
        return -1
    else:
        return 0

def cci(row):
    if row['CCI_14_0.015'] < -100:
        return 1
    elif row['CCI_14_0.015'] > 100:
        return -1
    else:
        return 0

def ao(row):
    if row['AO_5_34'] > 0:
        return 1
    elif row['AO_5_34'] < 0:
        return -1