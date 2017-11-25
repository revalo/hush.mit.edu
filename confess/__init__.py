import pytz
from pytz import timezone
from tzlocal import get_localzone

from flask import Flask
from flask_humanize import Humanize

app = Flask(__name__)
h = Humanize(app)

from flask import request
from werkzeug import url_encode

import confess.config as config
import confess.constants as constants
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['APP_NAME'] = config.APP_NAME
app.config['RECAPTCHA_KEY'] = constants.RECAPTCHA_KEY
app.config['FACEBOOK'] = config.ENABLE_FACEBOOK
app.config['FACEBOOK_LINK'] = 'http://facebook.com/' + config.FACEBOOK_PAGE_ID
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

# To get newlines
import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

app.jinja_env.filters['datetimefilter'] = display_date

from confess.models import db
db.app = app
db.init_app(app)

if config.ENABLE_FACEBOOK:
    import confess.facebook_worker

import confess.controllers # registers controllers
