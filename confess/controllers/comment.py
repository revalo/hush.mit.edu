from confess import app
from confess.utils import *
from confess.constants import *
from confess.models.user import *
from confess.models.post import *
from confess.models.vote import *
from confess.models.comment import *
from confess.controllers.post import post_validation

import os
import json
import random
import datetime

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

@app.route('/comment/<int:p_id>', methods=['POST'])
@requires_auth()
def post_main_comment(p_id):
    error = ""
    if 'message' not in request.form:
        return "Incorrect POST data.", 400
    post = Post.query.filter_by(id=p_id).first()
    if not post:
        return "Post doesn't exist.", 400

    # XXX This is sketch, because it defaults to not being anonymous.
    anonymous = False
    if "anonymous" in request.form:
        anonymous = True

    message = request.form['message']
    val, e = post_validation(message, user.last_post)
    if not validate_recaptcha(request.form):
        error = "Incorrect RECAPTCHA."
    elif not val:
        error = e
    else:
        u = None
        if not anonymous:
            u = user.id
        n = datetime.datetime.now()

        # Validation successful!
        c = Comment(post_id=p_id,
                    message=message,
                    timestamp=n,
                    upvotes=0,
                    downvotes=0,
                    user=u)

        db.session.add(c)
        db.session.commit()

    return redirect('/?%i&error=%s' % (p_id, error))

@app.route('/reply/<int:c_id>', methods=['POST'])
@requires_auth()
def post_reply(c_id):
    error = ""
    if 'message' not in request.form:
        return "Incorrect POST data.", 400
    parent = Comment.query.filter_by(id=c_id).first()
    if not parent:
        return "Comment doesn't exist.", 400

    # XXX This is sketch, because it defaults to not being anonymous.
    anonymous = False
    if "anonymous" in request.form:
        anonymous = True

    message = request.form['message']
    val, e = post_validation(message, user.last_post)
    if not val:
        error = e
    else:
        u = None
        if not anonymous:
            u = user.id

        n = datetime.datetime.now()
        c = Comment(post_id=parent.post_id,
            message=message,
            timestamp=n,
            upvotes=0,
            downvotes=0,
            parent=parent,
            user=u)

        db.session.add(c)
        db.session.commit()

    return redirect('/?%i&error=%s' % (parent.post_id, error))


def comment_dfs(comment, user, level=0):
    d = []
    # Do something
    for reply in comment.replies.order_by(Comment.hn_score.desc()):
        value = 0
        if user:
            v = CommentVote.query.filter((CommentVote.comment_id == reply.id) & (CommentVote.user == user.id)).first()
            if v:
                value = v.value

        kerb = User.query.filter_by(id=reply.user).first()
        if kerb:
            kerb = kerb.email.split('@')[0]

        d.append({'comment': reply, 'children': comment_dfs(reply, user, level+1), 'level': level+1, 'vote': value, 'kerb': kerb})
    return d

# XXX This is O(n) queries, yikes
def get_comment_dict(p_id, user):
    d = []
    for comment in Comment.query.filter((Comment.post_id == p_id) & (Comment.parent == None)).order_by(Comment.hn_score.desc()):
        value = 0
        if user:
            v = CommentVote.query.filter((CommentVote.comment_id == comment.id) & (CommentVote.user == user.id)).first()
            if v:
                value = v.value

        kerb = User.query.filter_by(id=comment.user).first()
        if kerb:
            kerb = kerb.email.split('@')[0]

        d.append({'comment': comment, 'children': comment_dfs(comment, user), 'level': 0, 'vote': value, 'kerb': kerb})
    return d