from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func, case, text, Numeric
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    ## Only stored if the user unchecked the anonymous option
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    @hybrid_property
    def hn_score(self):
        s = self.upvotes - self.downvotes
        item_hour_age = (datetime.datetime.now() - self.timestamp).total_seconds() / 3600.0
        return (s - 1) / (item_hour_age + 2)**1.8

    @hn_score.expression
    def hn_score(cls):
        s = cls.upvotes - cls.downvotes
        item_hour_age = -1 * func.date_part('epoch', func.age(cls.timestamp, func.current_timestamp())) / 3600
        return (s - 1) / func.power((item_hour_age+2), 1.8)