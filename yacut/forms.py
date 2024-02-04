from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 1256)]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
