from datetime import datetime

from yacut import db
from settings import FIELDS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(1256))
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            custom_id=self.short
        )

    def from_dict(self, data):
        for model_field, api_field in FIELDS.items():
            if api_field in data:
                setattr(self, model_field, data[api_field])
