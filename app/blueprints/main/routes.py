from flask import render_template, g

from . import bp
from app import app
from app.forms import UserSearchForm




@app.before_request
def before_request():
    g.user_search_form = UserSearchForm()

@bp.route('/')
def home():
    return render_template('index.jinja')

@bp.route('/marketplace')
def marketplace():
    return render_template('marketplace.jinja')