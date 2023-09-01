from datetime import datetime, timedelta
from bingx import getCurrencyDataFrame

threeDaysAgo = datetime.now() - timedelta(days=3)
threeDaysAgoInteger = int(threeDaysAgo.timestamp() * 1000)
symbol = 'CYBER-USDT'
currencyParams = {
    "symbol": symbol,
    "interval": "1d",
    # "startTime": threeDaysAgoInteger,
}
testDf = getCurrencyDataFrame(currencyParams)