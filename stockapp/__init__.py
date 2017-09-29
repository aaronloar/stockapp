from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

import stockapp.views.basic_view
import stockapp.views.view_ten_mm
import stockapp.calcs.calculations
