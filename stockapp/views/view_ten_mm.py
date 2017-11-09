
import pprint
import time

import requests
from flask import render_template

from stockapp import app
from stockapp.calcs import calculations, av_calls


# https://www.alphavantage.co/documentation/


@app.route('/av/<symbol>')
def stock_info(symbol):
    print("Getting info for: {}".format(symbol))
    sma = av_calls.sma200(symbol)
    rsi = av_calls.rsi3(symbol)

    return render_template("stockdata.html", symbol=symbol, sma=sma, rsi=rsi)


@app.route('/stock/<symbol>')
def get_daily(symbol):

    sma_period = 200
    rsi_period = 3
    atr_period = 14

    params = {"function": "TIME_SERIES_DAILY",
              "symbol": str(symbol).upper(),
              "outputsize": "full",
              "data_type": "json",
              "apikey": app.config["API_KEY"]
              }

    print("Getting info for: {}".format(symbol))
    ts = time.time()
    r = requests.get(app.config["URL"], params=params)

    print("{} - {}".format(r.status_code, time.time() - ts))
    r.raise_for_status()

    meta = r.json()['Meta Data']
    data = r.json()['Time Series (Daily)']

    f_meta = pprint.pformat(meta, indent=2, width=100)
    f_data = pprint.pformat(data, indent=2, width=70)

    # close, close_date = calculations.close_price(symbol)

    close_date = sorted(data.keys())[-1]
    close = data[close_date]
    close_prev = float(data[sorted(data.keys())[-2]]["4. close"])

    for k, v in close.items():
        close[k] = float(v)

    ts = time.time()

    sma = calculations.sma(data, sma_period)
    atr = calculations.atr(data, atr_period)
    rsi = calculations.rsi(data, rsi_period)
    low3 = calculations.low3(data)
    stop = calculations.get_stop(low3, atr)
    max_loss = close["4. close"] - stop
    print("Calculation time: {}".format(time.time() - ts))

    info = {"symbol": symbol,
            "meta": f_meta,
            # "data": f_data,
            "close_price": "{:.2f}".format(close["4. close"]),
            "close_change": "{:.2f}".format(close["4. close"] - close_prev),
            "close_date": close_date,
            "c_sma": "{:.3f}".format(sma),
            "c_rsi": "{:.3f}".format(rsi),
            "c_atr": "{:.4f}".format(atr),
            "c_low3": "{:.2f}".format(low3),
            "c_stop": "{:.2f}".format(stop),
            "c_max_loss": "{:.2f}".format(max_loss)

            }

    ts = time.time()
    rt = render_template("daily.html", info=info)
    print("Render time: {}".format(time.time() - ts))
    return rt


@app.route('/daily/<symbol>')
def raw_daily(symbol):
    sma_period = 200
    rsi_period = 3
    atr_period = 14

    params = {"function": "TIME_SERIES_INTRADAY",
              "symbol": str(symbol).upper(),
              "interval": "1min",
              "datatype": "json",
              "apikey": app.config["API_KEY"]
              }

    print("Getting info for: {}".format(symbol))
    ts = time.time()
    r = requests.get(app.config["URL"], params=params)

    print("{} - {}".format(r.status_code, time.time() - ts))
    r.raise_for_status()

    data = r.json()

    dc = []
    for k in data.keys():
        dc.append(len(data[k]))

    data['Meta Data']["7. Samples"] = dc

    f_data = pprint.pformat(data, indent=2, width=100)

    return render_template("raw.html", f_d=f_data)


@app.route('/compare/<symbol>')
def compare_values(symbol):

    sma_period = 200
    rsi_period = 3
    atr_period = 14

    # Get Full Data
    params = {"function": "TIME_SERIES_DAILY",
              "symbol": str(symbol).upper(),
              "outputsize": "full",
              "data_type": "json",
              "apikey": app.config["API_KEY"]
              }

    print("Getting info for: {}".format(symbol))
    ts = time.time()
    r = requests.get(app.config["URL"], params=params)

    print("{} - {}".format(r.status_code, time.time() - ts))
    r.raise_for_status()

    data = r.json()['Time Series (Daily)']

    close_date = sorted(data.keys())[-1]
    close = data[close_date]
    close_prev = float(data[sorted(data.keys())[-2]]["4. close"])

    for k, v in close.items():
        close[k] = float(v)

    ts = time.time()

    c_sma = calculations.sma(data, sma_period)
    c_atr = calculations.atr(data, atr_period)
    c_rsi = calculations.rsi(data, rsi_period)
    c_low3 = calculations.low3(data)
    print("Calculation time: {}".format(time.time() - ts))

    # get rsi, sma, atr, and close from AV
    ts = time.time()
    av_sma = av_calls.sma200(symbol)
    av_atr = av_calls.atr14(symbol)
    av_rsi = av_calls.rsi3(symbol)
    av_low3 = av_calls.low3(symbol)
    print("AV time: {}".format(time.time() - ts))

    info = {"symbol": symbol,
            "close_price": "{:.2f}".format(close["4. close"]),
            "close_change": "{:.2f}".format(close["4. close"] - close_prev),
            "close_date": close_date,
            "c_sma": "{:.3f}".format(c_sma),
            "c_rsi": "{:.3f}".format(c_rsi),
            "c_atr": "{:.4f}".format(c_atr),
            "c_low3": "{:.2f}".format(c_low3),
            "av_sma": "{:.3f}".format(av_sma),
            "av_rsi": "{:.3f}".format(av_rsi),
            "av_atr": "{:.4f}".format(av_atr),
            "av_low3": "{:.2f}".format(av_low3),
            }

    ts = time.time()
    rt = render_template("compare.html", info=info)
    print("Render time: {}".format(time.time() - ts))
    return rt


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
