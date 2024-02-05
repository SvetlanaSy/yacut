from datetime import datetime

from flask import url_for
from yacut import db
from settings import FIELDS, ORIGINAL_MAX_STRING, SHORT_MAX_STRING


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_STRING))
    short = db.Column(db.String(SHORT_MAX_STRING))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def from_dict(self, data):
        for model_field, api_field in FIELDS.items():
            if api_field in data:
                setattr(self, model_field, data[api_field])
