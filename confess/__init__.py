import pytz
from pytz import timezone
from tzlocal import get_localzone

from flask import Flask
app = Flask(__name__)

from flask import request
from werkzeug import url_encode

import confess.config as config
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APP_NAME'] = config.APP_NAME
app.secret_key = config.SECRET

# Debug
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = config.DEBUG

# Jinja Custom Filters
def display_date(value):
    return value.strftime("%b %d, %Y %I:%M %p")

# Jinja Custom Helpers
@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))

app.jinja_env.filters['datetimefilter'] = display_date

from confess.models import db
db.app = app
db.init_app(app)

import confess.controllers # registers controllers
