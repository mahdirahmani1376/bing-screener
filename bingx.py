import pandas as pd
from crypto_meter import get_crypto_meter_dataframe
from helper_functions import *
from coin_market_cap import get_coin_market_cap_df

with_crypto_meter = False

# h4_time_frame = "4h"
# h1_time_frame = "1h"
# d1_time_frame = "1d"
# time_frame = d1_time_frame

if with_crypto_meter:
    df_crypto_meter = get_crypto_meter_dataframe()

df_coin_market_cap = get_coin_market_cap_df()


async def main(dfAllCurrencies):
    payload = {}
    path = '/openApi/spot/v1/market/kline'
    method = "GET"
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in (dfAllCurrencies['symbol']):
            currencyParams = {
                "symbol": f"{i}",
                "interval": f"{time_frame}",
                "startTime": startTime,
            }
            paramsStr = praseParam(currencyParams)
            tasks.append(
                asyncio.ensure_future(sendAsyncRequest(session, path, paramsStr, currencyParams=currencyParams)))

        results = []
        # results = await asyncio.gather(*tasks)
        for f in tqdm.as_completed(tasks, total=len(tasks)):
            results.append(await f)

        return results


async def sendAsyncRequest(session, path, urlpa, currencyParams):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    async with limiter:
        try:
            async with session.get(url) as response:
                text = await response.text()
                return getCurrencyDataFrame(text, currencyParams)
        except Exception as e:
            print(e)


##################################################################################################
def getCurrencyDataFrame(data, currencyParams):
    dfCurrency = pd.DataFrame(json.loads(data)['data'])
    ##########################################normalizing data###########################################################
    dfCurrency.columns = defaultColumns
    dfTimeStamp = dfCurrency.copy()
    dfTimeStamp['symbol'] = currencyParams['symbol']
    dfTimeStamp['candlestick_chart_close_time'] = dfTimeStamp['candlestick_chart_close_time'].apply(convertToTimeStamp)
    dfTimeStamp['candlestick_chart_open_time'] = dfTimeStamp['candlestick_chart_open_time'].apply(convertToTimeStamp)
    dfTimeStamp['volume'] = dfTimeStamp['volume'].apply(lambda x: x / 1000000)
    dfTimeStamp2 = dfTimeStamp.set_index('candlestick_chart_close_time')
    ##########################################normalizing data###########################################################
    dfTimeStamp2['strong_bullish'] = dfTimeStamp2.apply(strongBullishCandle, axis=1)
    dfTimeStamp2['strong_bearish'] = dfTimeStamp2.apply(strongBerishCandle, axis=1)
    dfTimeStamp2['symbol'] = currencyParams['symbol']
    dfvolume = dfTimeStamp2.copy()
    dfvolume = dfvolume.sort_index(ascending=False)
    dfvolume['last_day_volume'] = dfvolume['volume'].shift(periods=-1)
    dfvolume['last_day_open'] = dfvolume['open'].shift(periods=-1)
    dfvolume['last_day_close'] = dfvolume['close'].shift(periods=-1)
    dfvolume['last_day_high'] = dfvolume['high'].shift(periods=-1)
    dfvolume['last_day_low'] = dfvolume['low'].shift(periods=-1)
    dfvolume['strong_volume'] = dfvolume.apply(lambda x: x['volume'] > 3 * (x['last_day_volume']), axis=1)
    dfvolume['strong_bullish_signal'] = dfvolume.apply(strongBullishSignal, axis=1)
    dfvolume['strong_bearish_signal'] = dfvolume.apply(strongBearishSignal, axis=1)
    dfvolume['strong_ratio'] = dfvolume.apply(strongRatio, axis=1)

    strongBullishCloseList = []
    strongBearishCloseList = []
    for index, value in enumerate(dfvolume['close']):
        bullishValueToAppend = value > dfvolume.iloc[index + 1:index + 7]['close'].max()
        bearishValueToAppend = value < dfvolume.iloc[index + 1:index + 7]['close'].min()
        strongBullishCloseList.append(bullishValueToAppend)
        strongBearishCloseList.append(bearishValueToAppend)

    dfvolume['strong_bullish_close_past_bars_before'] = strongBullishCloseList
    dfvolume['strong_bearish_close_past_bars_before'] = strongBearishCloseList

    df_return = dfvolume.iloc[[1][:]]
    df_volume_cmc = pd.merge(left=df_return.reset_index(), right=df_coin_market_cap, left_on='symbol', right_on='symbol',
                             how='left').set_index('candlestick_chart_close_time')

    with pd.ExcelWriter(f"data/{time_frame}/{currencyParams['symbol']}.xlsx") as dfVolumeWriter:
        dfvolume.to_excel(dfVolumeWriter)

    if with_crypto_meter:
        return pd.merge(df_volume_cmc.reset_index(), df_crypto_meter, how='left', left_on='symbol',
                        right_on='name').set_index('candlestick_chart_close_time')
    else:
        return df_volume_cmc


###################################################################################################################

if __name__ == '__main__':
    dfAllCurrencies = pd.json_normalize(json.loads(getAllCurrencies())['data']['symbols'])
    ScreenerDf = pd.DataFrame([], columns=defaultColumns, index=['candlestick_chart_close_time'])
    startTime = datetime.now() - timedelta(days=7)
    startTime = int(startTime.timestamp() * 1000)
    results = asyncio.run(main(dfAllCurrencies))
    finalDf = pd.concat(results)

    with pd.ExcelWriter(f"screener_data_{time_frame}.xlsx") as writer:
        finalDf.to_excel(writer)
