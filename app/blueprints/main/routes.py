from flask import render_template, g, send_from_directory
import os
from . import bp
from app import app
from app.forms import UserSearchForm


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.before_request
def before_request():
    g.user_search_form = UserSearchForm()

@bp.route('/')
def home():
    return render_template('index.jinja')

@bp.route('/marketplace')
def marketplace():
    return render_template('marketplace.jinja')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')