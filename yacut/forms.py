from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from settings import ORIGINAL_MAX_STRING, ORIGINAL_MIN_STRING, SHORT_MAX_STRING


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(ORIGINAL_MIN_STRING, ORIGINAL_MAX_STRING)]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[Length(ORIGINAL_MIN_STRING, SHORT_MAX_STRING), Optional()]
    )
    submit = SubmitField('Создать')
