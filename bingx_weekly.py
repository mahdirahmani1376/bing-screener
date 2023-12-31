import os

import pandas as pd
import pandas_ta as ta
from helper_functions import *
from coin_market_cap import get_coin_market_cap_df
from indicator_functions import adx_signal, atr_signal

pd.options.mode.chained_assignment = None  # default='warn'

now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

count_of_strong_close_bars = 4

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
    df = df.set_index('candlestick_chart_close_time').sort_index(ascending=False)
    ##########################################normalizing data###########################################################
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
    volume_coin_mcap = ""
    rank = ""
    volume_coin_mcap_series = df_coin_market_cap[df_coin_market_cap['symbol'] == df['symbol'].values[0]][
        'volume_mcap'].values
    if len(volume_coin_mcap_series) > 0:
        rank = df_coin_market_cap[df_coin_market_cap['symbol'] == df['symbol'].values[0]]['cmc_rank'].values[0]
        volume_coin_mcap = round(volume_coin_mcap_series[0], 3)

    df['volume_coin_mcap'] = volume_coin_mcap
    df['rank'] = rank
    ###########################################calculate_percent_changes###########################################
    close_column_loc = df.columns.get_loc('close')

    weekly_performance = calculate_percent_change(df, 1, close_column_loc)
    monthly_performance = calculate_percent_change(df, 4, close_column_loc)
    three_month_performance = calculate_percent_change(df, 12, close_column_loc)
    six_month_performance = calculate_percent_change(df, 24, close_column_loc)
    twelve_month_performance = calculate_percent_change(df, 48, close_column_loc)

    df_return = df.iloc[[1][:]]
    df_return['weekly_performance'] = weekly_performance
    df_return['monthly_performance'] = monthly_performance
    df_return['three_month_performance'] = three_month_performance
    df_return['six_month_performance'] = six_month_performance
    df_return['twelve_month_performance'] = twelve_month_performance

    df_volume_cmc = pd.merge(left=df_return.reset_index(), right=df_coin_market_cap, left_on='symbol',
                             right_on='symbol',
                             how='left').set_index('candlestick_chart_close_time')

    df_save_dir = f"data/{time_frame}"
    if not os.path.exists(df_save_dir):
        os.makedirs(df_save_dir)


    with pd.ExcelWriter(f"{df_save_dir}/{currencyParams['symbol']}.xlsx") as dfWriter:
        df.to_excel(dfWriter)

    savePathBullish = f"charts/{time_frame}/all/{now}"
    path = getSavePath(savePathBullish, df)
    saveCandleStickChart(df, path)

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
    else:
        startTime = datetime.now() - timedelta(days=365)

    startTime = int(startTime.timestamp() * 1000)
    results = asyncio.run(main(dfAllCurrencies))
    finalDf = pd.concat(results)

    with pd.ExcelWriter(f"data/screener_data_{time_frame}.xlsx") as writer:
        finalDf.to_excel(writer)
