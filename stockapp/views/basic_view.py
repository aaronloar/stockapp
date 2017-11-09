

from flask import render_template
# import requests
import sys

from stockapp import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/cakes')
def cakes():
    return 'Yummy cakes!!'


@app.route('/version')
def version():
    return sys.version


@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)
