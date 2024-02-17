from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_unique_short_id, get_short_url


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
    data['custom_id'] = generate_unique_short_id(data)
    if get_short_url(data['custom_id']):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
