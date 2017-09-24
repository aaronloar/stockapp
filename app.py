from flask import Flask, render_template
import requests

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
def sma(symbol):

    # https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=15min&time_period=10&series_type=close&apikey=demo

    params = {
        "function": "SMA",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 200,
        "series_type": "close",
        "apikey": API_KEY
    }

    r = requests.get(URL, params=params)
    print(r.status_code)
    print(r.url)
    print(type(r.text))
    data = r.json()
    print(type(data))
    print(len(data["Technical Analysis: SMA"]))

    # ToDo: parse through SMA returned data (by date "2017-09-22": 123.456)
    # ToDo: find latest sample
    # ToDo: Start on the next values...

    return render_template("stockdata.html", symbol=symbol, data=data["Technical Analysis: SMA"])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


