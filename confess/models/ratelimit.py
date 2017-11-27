from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

class RateLimit(db.Model):
    ip = db.Column(db.String(16), primary_key=True)
    last_request = db.Column(db.DateTime)