import uuid
import jwt
import os
from confess.config import *
from confess.constants import *
from confess.models.user import *
from flask import (redirect, request)
from functools import wraps
import datetime
import requests
from netaddr import *

# Import Whitelisted CIDR cache
mit_networks = []
with open('confess/static/mit_cidr.txt', 'r') as f:
    for line in f:
        mit_networks.append(IPNetwork(line.strip()))

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def encode_token(user):
    return jwt.encode({'id': user.id, 'email': user.email, 'roll': gen_uuid()}, SECRET, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])['id']

epoch = datetime.datetime(1970, 1, 1)
def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def requires_auth():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                except Exception as e:
                    return redirect('/login?redirect='+request.url)
                user = User.query.filter_by(id=decoded).first()
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                return redirect('/login')

        return decorated
    return decorator

def get_user():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                except Exception as e:
                    # FIXME Repeated code
                    f.__globals__['user'] = None
                    return f(*args, **kwargs)
                user = User.query.filter_by(id=decoded).first()
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                f.__globals__['user'] = None
                return f(*args, **kwargs)

        return decorated
    return decorator

def requires_auth_s():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = args[0]
            if 'jwt' in data:
                try:
                    decoded = decode_token(data['jwt'])
                except Exception as e:
                    disconnect()
                    return
                user = User.query.filter_by(id=decoded).first()
                kwargs['user'] = user
                return f(*args, **kwargs)
            else:
                disconnect()
                return

        return decorated
    return decorator

def val_form_keys(keys):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            for key in keys:
                if not key in request.form:
                    return "Missing: " + key, 400
                kwargs[key] = request.form[key]
            return f(*args, **kwargs)

        return decorated
    return decorator

def get_ts(dt):
    return (dt-datetime.datetime(1970,1,1)).total_seconds()

def validate_recaptcha(form):
    if "g-recaptcha-response" not in form:
        return False
    response = form['g-recaptcha-response']
    api = "https://www.google.com/recaptcha/api/siteverify"
    r = requests.post(api, data={'secret': RECAPTCHA_SECRET, 'response': response})
    j = r.json()
    return j['success']

def get_ip(request):
    # This is to handle nginx being a proxy for this app.
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def is_mit(request):
    ip = get_ip(request) 

    # Turn it into a netaddr object
    try:
        ip = IPAddress(ip)
    except:
        return False

    for network in mit_networks:
        if ip in network:
            return True
            
    return False

