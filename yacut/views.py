import string
import random

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('urlmap.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        flash('Такая ссылка уже существует!')
        return render_template('urlmap.html', form=form)
    urlmap = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return render_template('urlmap.html', url=urlmap, form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    urlmap = URLMap.query.filter_by(short=custom_id).first_or_404()
    return redirect(urlmap.original)
