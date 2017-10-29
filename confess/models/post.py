from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import func, case, text, Numeric
from datetime import datetime, timedelta
from math import log
from confess.utils import *
import datetime

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)

    # Functional ways to calculate 'hotness'
    @hybrid_property
    def reddit_score(self):
        s = self.upvotes - self.downvotes
        order = func.log(10, func.greatest(func.abs(s), 1))
        sign = func.sign(s)
        seconds = func.date_part('epoch', self.timestamp) - 1134028003

        return func.round(func.cast(sign * order + seconds / 45000, Numeric), 7)

    @hybrid_property
    def hn_score(self):
        s = self.upvotes - self.downvotes
        item_hour_age = func.date_part('epoch', func.age(self.timestamp, func.current_timestamp())) / 3600
        return (s - 1) / func.power((item_hour_age+2), 1.8)

    @hybrid_property
    def top(self):
        return self.upvotes - self.downvotes