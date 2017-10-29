from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    last_post = db.Column(db.DateTime)
