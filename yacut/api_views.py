from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Ссылка с указанным short_id не найдена', 404)
    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if 'custom_id' in data and URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Такая ссылка уже есть в базе данных')
    if data.get('custom_id') is None:
        data['custom_id'] = get_unique_short_id()
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
