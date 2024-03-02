from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_short_id, get_short_url


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
    original = data['url']
    short = data.get('custom_id')
    try:
        data['custom_id'] = create_short_id(original, short)
    except ValueError as e:
        raise InvalidAPIUsage(f'{e}')
    urlmap.from_dict(data)
    return jsonify(urlmap.to_dict()), 201
