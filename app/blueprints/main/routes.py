from flask import render_template, g, send_from_directory
import os
from . import bp
from app import app
from app.forms import UserSearchForm


# STATIC FOLDER ROUTE/FAVICON HELPER =========================================
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# GLOBAL/SEARCH FORM ROUTE ===================================================
@app.before_request
def before_request():
    g.user_search_form = UserSearchForm()

# HOME ROUTE ===================================================
@bp.route('/')
def home():
    return render_template('index.jinja')

# MARKETPLACE ROUTE ===================================================
@bp.route('/marketplace')
def marketplace():
    return render_template('marketplace.jinja')

# FAVICON ROUTE ===================================================
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')