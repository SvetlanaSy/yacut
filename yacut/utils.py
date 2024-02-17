import random

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import URL_SYMBOLS, URL_LENGTH, SHORT_MAX_LENGTH


def get_short_url(custom_id):
    return URLMap.query.filter_by(short=custom_id).first()


def generate_unique_short_id(data):
    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        return ''.join(random.choices(URL_SYMBOLS, k=URL_LENGTH))
    if len(data['custom_id']) > SHORT_MAX_LENGTH:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if not all((symbol in URL_SYMBOLS) for symbol in data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    return data['custom_id']
