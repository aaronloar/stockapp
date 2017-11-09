
import os

APP_TITLE = "10MM Stock Info"
APP_AUTHOR = "Aaron Loar"
APP_EMAIL = "aaronloar@gmail.com"
APP_DATE = "September, 2017"

VERSION = 0.1

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
