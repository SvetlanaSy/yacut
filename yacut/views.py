from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap
from .utils import generate_short_id, get_short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('urlmap.html', form=form)
    original = form.original_link.data
    custom_id = form.custom_id.data
    try:
        custom_id = generate_short_id(original, custom_id)
    except ValueError:
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('urlmap.html', form=form)
    urlmap = URLMap(
        original=form.original_link.data,
        short=custom_id)
    return render_template('urlmap.html', url=urlmap, form=form)


@app.route('/<string:short_link>')
def redirect_view(short_link):
    if not get_short_url(short_link):
        abort(404)
    return redirect(get_short_url(short_link).original)
