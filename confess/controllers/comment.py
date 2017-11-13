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

    message = request.form['message']
    val, e = post_validation(message, user.last_post)
    if not val:
        error = e
    else:
        n = datetime.datetime.now()
        # Validation successful!
        c = Comment(post_id=p_id,
                    message=message,
                    timestamp=n,
                    upvotes=0,
                    downvotes=0)

        user.last_post = n

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

    message = request.form['message']
    val, e = post_validation(message, user.last_post)
    if not val:
        error = e
    else:
        n = datetime.datetime.now()
        c = Comment(post_id=parent.post_id,
            message=message,
            timestamp=n,
            upvotes=0,
            downvotes=0,
            parent=parent)
        user.last_post = n

        db.session.add(c)
        db.session.commit()

    return redirect('/?%i&error=%s' % (parent.post_id, error))


def comment_dfs(comment, level=0):
    d = []
    # Do something
    for reply in comment.replies:
        d.append({'comment': reply, 'children': comment_dfs(reply, level+1), 'level': level+1})
    return d

# XXX This is O(n) queries, yikes
def get_comment_dict(p_id):
    d = []
    for comment in Comment.query.filter_by(parent=None).order_by(Comment.hn_score.desc()):
        d.append({'comment': comment, 'children': comment_dfs(comment), 'level': 0})
    return d