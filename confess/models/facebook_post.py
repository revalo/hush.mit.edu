from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

class FacebookPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))