import pprint

import sys
import requests
from flask import render_template

import av_calls
from stockapp import app
from stockapp.calcs import calculations

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
    r = requests.get(app.config["URL"], params=params)

    if r.status_code != 200:
        print("Error getting daily data: {}\n{}".format(r.status_code, r.text))
        return render_template("daily.html", symbol=symbol,
                               meta="Error code: {}".format(r.status_code),
                               data="{}".format(r.text))
    else:
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

        sma = calculations.sma(data, sma_period)
        atr = calculations.atr(data, atr_period)
        rsi = calculations.rsi(data, rsi_period)
        low3 = calculations.low3(data)
        stop = calculations.get_stop(low3, atr)
        max_loss = close["4. close"] - stop

        info = {"symbol": symbol,
                "meta": f_meta,
                "data": f_data,
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

        return render_template("daily.html", info=info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
