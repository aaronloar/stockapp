from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from stockapp.views import view_ten_mm, basic_view
from stockapp.models import stock_model
import stockapp.calcs.calculations

