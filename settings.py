import os
import string

FIELDS = {'original': 'url', 'short': 'custom_id'}
REGULAR_SYMBOLS = r'^[a-zA-Z\d]{1,16}$'
SYMBOLS = string.ascii_letters + string.digits
SYMBOLS_NUMBER = 6
ORIGINAL_MAX_STRING = 1256
SHORT_MAX_STRING = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
