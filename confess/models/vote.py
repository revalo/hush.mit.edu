from confess.models import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

UPVOTE = 1
DOWNVOTE = -1

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)

class CommentVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)