from flask import Flask, render_template
import requests
import pprint
import calculations
import av_calls

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


@app.route('/av/<symbol>')
def stock_info(symbol):
    print("Getting info for: {}".format(symbol))
    sma = av_calls.sma200(symbol)
    rsi = av_calls.rsi3(symbol)

    return render_template("stockdata.html", symbol=symbol, sma=sma, rsi=rsi)


@app.route('/stock/<symbol>')
def get_daily(symbol):
    params = {"function": "TIME_SERIES_DAILY",
              "symbol": symbol,
              "outputsize": "full",
              "data_type": "json",
              "apikey": API_KEY
              }

    print("Getting info for: {}".format(symbol))
    r = requests.get(URL, params=params)

    if r.status_code != 200:
        print("Error getting daily data: {}\n{}".format(r.status_code, r.text))
        return render_template("daily.html", symbol=symbol,
                               meta="Error code: {}".format(r.status_code),
                               data="{}".format(r.text))

    meta = r.json()['Meta Data']
    data = r.json()['Time Series (Daily)']

    f_meta = pprint.pformat(meta, indent=2, width=100)

    return render_template("daily.html",
                           symbol=symbol,
                           meta=f_meta,
                           c_sma="{:.4f}".format(calculations.sma(data, 200)),
                           c_rsi="{:.4f}".format(calculations.rsi(data, 3)),
                           c_atr="{:.4f}".format(calculations.atr(data, 14)),
                           c_low3="{:.2f}".format(calculations.low3(data)),
                           )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


