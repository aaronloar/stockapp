import requests
from stockapp import app


def sma200(symbol):

    # https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=15min&time_period=10&series_type=close&apikey=demo

    params = {"function": "SMA",
              "symbol": str(symbol).upper(),
              "interval": "daily",
              "time_period": 200,
              "series_type": "close",
              "apikey": app.config["API_KEY"]
              }

    r = requests.get(app.config["URL"], params=params)
    if r.status_code != requests.codes.ok:
        print("Error getting SMA data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()['Technical Analysis: SMA']

    key = sorted(data)[-1]

    return float(data[key]["SMA"])


def rsi3(symbol):
    params = {"function": "RSI",
              "symbol": str(symbol).upper(),
              "interval": "daily",
              "time_period": 3,
              "series_type": "close",
              "apikey": app.config["API_KEY"]
              }

    r = requests.get(app.config["URL"], params=params)
    if r.status_code != requests.codes.ok:
        print("Error getting RSI data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()['Technical Analysis: RSI']

    key = sorted(data)[-1]

    return float(data[key]["RSI"])


def atr14(symbol):
    params = {"function": "ATR",
              "symbol": str(symbol).upper(),
              "interval": "daily",
              "time_period": 14,
              "series_type": "close",
              "apikey": app.config["API_KEY"]
              }

    r = requests.get(app.config["URL"], params=params)
    if r.status_code != requests.codes.ok:
        print("Error getting RSI data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()['Technical Analysis: ATR']

    key = sorted(data)[-1]

    return float(data[key]["ATR"])


def low3(symbol):
    params = {"function": "TIME_SERIES_DAILY",
              "symbol": str(symbol).upper(),
              "outputsize": "compact",
              "datatype": "json",
              "apikey": app.config["API_KEY"]
              }

    r = requests.get(app.config["URL"], params=params)
    if r.status_code != requests.codes.ok:
        print("Error getting RSI data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()['Time Series (Daily)']

    return min([float(data[x]['3. low']) for x in sorted(data)[-3:]])


