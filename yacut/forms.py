from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from settings import ORIGINAL_MAX_LENGTH, ORIGINAL_MIN_LENGTH, SHORT_MAX_LENGTH


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(ORIGINAL_MIN_LENGTH, ORIGINAL_MAX_LENGTH)]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[Length(ORIGINAL_MIN_LENGTH, SHORT_MAX_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
