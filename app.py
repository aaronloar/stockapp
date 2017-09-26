from flask import Flask, render_template
import requests
import pprint
import calculations

# https://www.alphavantage.co/documentation/

app = Flask(__name__)

URL = "https://www.alphavantage.co/query"
API_KEY = "CCJ9QRK2JHEB3EJ4"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cakes')
def cakes():
    return 'Yummy cakes!!'


@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)


@app.route('/stock/<symbol>')
def stock_info(symbol):
    print("Getting info for: {}".format(symbol))
    sma = sma200(symbol)
    rsi = rsi3(symbol)

    return render_template("stockdata.html", symbol=symbol, sma=sma, rsi=rsi)


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


@app.route('/daily/<symbol>')
def get_daily(symbol):
    params = {"function": "TIME_SERIES_DAILY",
              "symbol": symbol,
              "outputsize": "full",
              "time_period": 3,
              "data_type": "json",
              "apikey": API_KEY
              }

    r = requests.get(URL, params=params)
    meta = r.json()['Meta Data']
    data = r.json()['Time Series (Daily)']

    # l_data = [data[k] for k in sorted(data.keys())]

    f_meta = pprint.pformat(meta, indent=2, width=100)
    f_data = pprint.pformat(data, indent=2, width=40)

    if r.status_code != 200:
        print("Error getting RSI data: {}\n{}".format(r.status_code, r.text))
        return render_template("daily.html", symbol=symbol,
                               meta="Error code: {}".format(r.status_code),
                               data="{}".format(r.text))

    return render_template("daily.html",
                           symbol=symbol,
                           meta=f_meta,
                           data=f_data,
                           sma=sma200(symbol),
                           c_sma=calculations.sma(data, 200),
                           rsi=rsi3(symbol),
                           c_rsi=calculations.rsi(data, 3))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


