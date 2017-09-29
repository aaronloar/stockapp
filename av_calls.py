import requests

API_KEY = None
URL = None

def sma200(symbol):

    # https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=15min&time_period=10&series_type=close&apikey=demo

    params = {"function": "SMA",
              "symbol": symbol,
              "interval": "daily",
              "time_period": 200,
              "series_type": "close",
              "apikey": API_KEY
              }

    r = requests.get(URL, params=params)
    if r.status_code != 200:
        print("Error getting SMA data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()
    sma_dict = data['Technical Analysis: SMA']
    # print(sorted(sma_dict))
    key = sorted(sma_dict.keys())[-1]
    most_recent = {key: sma_dict[key]}
    print(most_recent)

    return most_recent


def rsi3(symbol):
    params = {"function": "RSI",
              "symbol": symbol,
              "interval": "daily",
              "time_period": 3,
              "series_type": "close",
              "apikey": API_KEY
              }

    r = requests.get(URL, params=params)
    if r.status_code != 200:
        print("Error getting RSI data: {}\n{}".format(r.status_code, r.text))
        return "Error"

    data = r.json()['Technical Analysis: RSI']

    key = sorted(data)[-1]

    return {key: data[key]}
