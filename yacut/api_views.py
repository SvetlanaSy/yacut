from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from settings import FORMAT_SYMBOLS


def short_url_exist(short_url):
    return URLMap.query.filter_by(short=short_url).first()


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    if not short_id:
        raise InvalidAPIUsage('Укажите short_id', 400)
    urlmap = URLMap.query.filter_by(short=short_id).first()
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
    if 'custom_id' in data:
        if short_url_exist(data['custom_id']):
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        if len(str(data.get('custom_id'))) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
        if not all((symbol in FORMAT_SYMBOLS) for symbol in str(data['custom_id'])):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
