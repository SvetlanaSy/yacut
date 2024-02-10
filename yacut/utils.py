import random

from .models import URLMap
from settings import URL_SYMBOLS, URL_LENGTH


def get_unique_short_id():
    return ''.join(random.choices(URL_SYMBOLS, k=URL_LENGTH))


def get_short_url(short_id):
    return URLMap.query.filter_by(short=short_id).first()
