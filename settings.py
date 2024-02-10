import os
import string

MODEL_VC_API_FIELDS = {'original': 'url', 'short': 'custom_id'}
URL_SYMBOLS = string.ascii_letters + string.digits
URL_LENGTH = 6
ORIGINAL_MIN_LENGTH = 1
ORIGINAL_MAX_LENGTH = 1256
SHORT_MAX_LENGTH = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
