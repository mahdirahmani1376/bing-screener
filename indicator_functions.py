import pandas_ta as ta

def adx_signal(row):
    try:
        if (row['DMP_14'] > row['DMN_14']) and (row['ADX_14'] > 20):
            return 1
        elif (row['DMN_14'] > row['DMP_14']) and (row['ADX_14'] > 20):
            return -1
        else:
            return 0
    except Exception as e:
        # print(e)
        return 0
def atr_signal(row):
    try:
        return (row['close'] - row['open']) > (3 * row['ATRr_14'])
    except Exception as e:
        # print(e)
        return False

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
def sma_50(row):
    if (row['price'] > row['SMA_50']):
        return 1
    else:
        return -1

def sma_100(row):
    if (row['price'] > row['SMA_100']):
        return 1
    else:
        return -1

def sma_200(row):
    if (row['price'] > row['SMA_200']):
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

def mom(row):
    if row['MOM_10'] > 0:
        return 1
    elif row['MOM_10'] < 0:
        return -1
    else:
        return 0

def stochastic(row):
    if row['STOCHRSIk_14_14_3_3'] < 20 and row['STOCHRSId_14_14_3_3'] < 20 and row['STOCHRSIk_14_14_3_3'] > row['STOCHRSId_14_14_3_3']:
        return 1
    elif row['STOCHRSIk_14_14_3_3'] > 80 and row['STOCHRSId_14_14_3_3'] > 80 and row['STOCHRSIk_14_14_3_3'] < row['STOCHRSId_14_14_3_3']:
        return -1
    else:
        return 0

def uo(row):
    if row['UO_7_14_28'] > 70:
        return 1
    elif row['UO_7_14_28'] < 30:
        return -1
    else:
        return 0

def technical_rating(row):
    moving_ratings = sma_20(row) + ema_20(row) / 2
    oscillator_ratings = rsi(row) + stochastic(row) + cci(row) + ao(row) + mom(row) + stochastic(row) + uo(row) / 7
    return moving_ratings + oscillator_ratings > 0

