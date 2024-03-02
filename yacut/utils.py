import random

from . import db
from .models import URLMap
from settings import URL_SYMBOLS, URL_LENGTH, SHORT_MAX_LENGTH


def get_short_url(custom_id):
    return URLMap.query.filter_by(short=custom_id).first()


def generate_short_id():
    return ''.join(random.choices(URL_SYMBOLS, k=URL_LENGTH))


def validate_short_id(short_url):
    if len(short_url) > SHORT_MAX_LENGTH:
        raise ValueError('Указано недопустимое имя для короткой ссылки')
    if not all((symbol in URL_SYMBOLS) for symbol in short_url):
        raise ValueError('Указано недопустимое имя для короткой ссылки')
    if get_short_url(short_url):
        raise ValueError('Предложенный вариант короткой ссылки уже существует.')


def save_to_db(url, short_url):
    urlmap = URLMap(original=url, short=short_url)
    db.session.add(urlmap)
    db.session.commit()


def create_short_id(url, short_url=None):
    if short_url is None or short_url == '':
        short_url = generate_short_id()
    validate_short_id(short_url)
    save_to_db(url, short_url)
    return short_url
