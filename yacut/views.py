import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from settings import SYMBOLS, SYMBOLS_NUMBER


def get_unique_short_id():
    return ''.join(random.choices(SYMBOLS, k=SYMBOLS_NUMBER))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('urlmap.html', form=form)
    custom_id = form.custom_id.data
    if custom_id is None or custom_id == '':
        custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('urlmap.html', form=form)
    urlmap = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return render_template('urlmap.html', url=urlmap, form=form)


@app.route('/<string:short_link>')
def redirect_view(short_link):
    urlmap = URLMap.query.filter_by(short=short_link).first()
    if not urlmap:
        abort(404)
    return redirect(urlmap.original)
