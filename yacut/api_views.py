from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, get_short_url
from settings import URL_SYMBOLS, SHORT_MAX_LENGTH


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    if not short_id:
        raise InvalidAPIUsage('Укажите short_id', 400)
    urlmap = get_short_url(short_id)
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    urlmap = URLMap()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    if get_short_url(data['custom_id']):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    if len(data.get('custom_id')) > SHORT_MAX_LENGTH:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if not all((symbol in URL_SYMBOLS) for symbol in data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
