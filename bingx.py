import pandas as pd
import pandas_ta as ta
from crypto_meter import get_crypto_meter_dataframe
from helper_functions import *
from coin_market_cap import get_coin_market_cap_df
from indicator_functions import adx_signal,atr_signal

with_crypto_meter = False

# h4_time_frame = "4h"
# h1_time_frame = "1h"
# d1_time_frame = "1d"
# time_frame = d1_time_frame
count_of_strong_close_bars = 6

if with_crypto_meter:
    df_crypto_meter = get_crypto_meter_dataframe()

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
    df = pd.DataFrame(json.loads(data)['data'])
    ##########################################normalizing data###########################################################
    df.columns = defaultColumns
    df['symbol'] = currencyParams['symbol']
    df['candlestick_chart_close_time'] = df['candlestick_chart_close_time'].apply(convertToTimeStamp)
    df['candlestick_chart_open_time'] = df['candlestick_chart_open_time'].apply(convertToTimeStamp)
    df['volume'] = df['volume'].apply(lambda x: x / 1000000)
    df = df.set_index('candlestick_chart_close_time').sort_index(ascending=True)
    #############################apllying indicators################################################
    df_adx = df.ta.adx(high=df['high'], low=df['low'], close=df['close'], length=14)
    df_atr = df.ta.atr()
    df = pd.concat([df, df_adx, df_atr], axis=1, join='inner')
    df['adx_rating'] = df.apply(adx_signal, axis=1)
    df['atr_rating'] = df.apply(atr_signal, axis=1)
    ##########################################normalizing data###########################################################
    df = df.sort_index(ascending=False)
    df['strong_bullish'] = df.apply(strongBullishCandle, axis=1)
    df['strong_bearish'] = df.apply(strongBerishCandle, axis=1)
    df['symbol'] = currencyParams['symbol']
    df['last_day_volume'] = df['volume'].shift(periods=-1)
    df['last_day_open'] = df['open'].shift(periods=-1)
    df['last_day_close'] = df['close'].shift(periods=-1)
    df['last_day_high'] = df['high'].shift(periods=-1)
    df['last_day_low'] = df['low'].shift(periods=-1)
    df['strong_volume'] = df.apply(lambda x: x['volume'] > 3 * (x['last_day_volume']), axis=1)
    df['strong_bullish_signal'] = df.apply(strongBullishSignal, axis=1)
    df['strong_bearish_signal'] = df.apply(strongBearishSignal, axis=1)
    df['strong_ratio'] = df.apply(strongRatio, axis=1)


    strongBullishCloseList = []
    strongBearishCloseList = []
    for index, value in enumerate(df['close']):
        bullishValueToAppend = value > df.iloc[index + 1:index + count_of_strong_close_bars]['close'].max()
        bearishValueToAppend = value < df.iloc[index + 1:index + count_of_strong_close_bars]['close'].min()
        strongBullishCloseList.append(bullishValueToAppend)
        strongBearishCloseList.append(bearishValueToAppend)

    df['strong_bullish_close_past_bars_before'] = strongBullishCloseList
    df['strong_bearish_close_past_bars_before'] = strongBearishCloseList
    ###########################################coin_market_cap#######################################################
    crypto_meter_data = ""
    if with_crypto_meter:
        volume_mcap = round(df[df['symbol'] == df['symbol'].values[0]]['volume_mcap'].values[0], 3)
        if pd.isna(volume_mcap):
            crypto_meter_data = f""
        else:
            crypto_meter_data = f"_v_{volume_mcap}"

    volume_coin_mcap = ""
    rank = ""
    volume_coin_mcap_series = df_coin_market_cap[df_coin_market_cap['symbol'] == df['symbol'].values[0]][
        'volume_mcap'].values
    if len(volume_coin_mcap_series) > 0:
        rank = df_coin_market_cap[df_coin_market_cap['symbol'] == df['symbol'].values[0]]['cmc_rank'].values[0]
        volume_coin_mcap = round(volume_coin_mcap_series[0], 3)

    df['volume_coin_mcap'] = volume_coin_mcap
    df['crypto_meter_data'] = crypto_meter_data
    df['rank'] = rank
    ###########################################coin_marrket_cap#######################################################


    df_return = df.iloc[[1][:]]
    df_volume_cmc = pd.merge(left=df_return.reset_index(), right=df_coin_market_cap, left_on='symbol', right_on='symbol',
                             how='left').set_index('candlestick_chart_close_time')

    with pd.ExcelWriter(f"data/{time_frame}/{currencyParams['symbol']}.xlsx") as dfWriter:
        df.to_excel(dfWriter)

    if with_crypto_meter:
        return pd.merge(df_volume_cmc.reset_index(), df_crypto_meter, how='left', left_on='symbol',
                        right_on='name').set_index('candlestick_chart_close_time')
    else:
        return df_volume_cmc


###################################################################################################################

if __name__ == '__main__':
    df_coin_market_cap = get_coin_market_cap_df()
    dfAllCurrencies = pd.json_normalize(json.loads(getAllCurrencies())['data']['symbols'])
    ScreenerDf = pd.DataFrame([], columns=defaultColumns, index=['candlestick_chart_close_time'])
    if time_frame == d1_time_frame:
        startTime = datetime.now() - timedelta(days=30)
    elif time_frame == h4_time_frame:
        startTime = datetime.now() - timedelta(days=14)
    elif time_frame == h1_time_frame:
        startTime = datetime.now() - timedelta(days=7)
    elif time_frame == m_15_time_frame:
        startTime = datetime.now() - timedelta(days=1)
        
    startTime = int(startTime.timestamp() * 1000)
    results = asyncio.run(main(dfAllCurrencies))
    finalDf = pd.concat(results)

    with pd.ExcelWriter(f"screener_data_{time_frame}.xlsx") as writer:
        finalDf.to_excel(writer)
