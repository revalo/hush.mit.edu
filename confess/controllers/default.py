from confess import app
from confess.utils import *
from confess.constants import *
from confess.models.user import *
from confess.models.post import *
from confess.models.vote import *
from confess.models.comment import *
from confess.controllers.comment import get_comment_dict 

import os
import json

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

# Display the home page
@app.route('/')
@get_user()
def index():
    mit = is_mit(request)

    # Find post id if any
    p_id = -1
    for k, v in request.args.items():
        if v == '':
            try:
                p_id = int(k)
            except Exception as e:
                pass

    if 'p' in request.args:
        try:
            p = int(request.args['p'])
        except Exception as e:
            return "Error"
    else:
        p = 0

    sel = 'hot'
    if 's' in request.args:
        s = request.args['s']
        if s == 'top':
            order = Post.top.desc()
            sel = s
        elif s == 'new':
            order = Post.timestamp.desc()
            sel = s
        else:
            order = Post.hn_score.desc()
    else:
        order = Post.hn_score.desc()

    if p_id < 0:
        posts = db.session.query(Post).order_by(order).limit(PAGE_SIZE).offset(PAGE_SIZE*p)
    else:
        posts = Post.query.filter_by(id=p_id)

    # This iteration is slow, but since it's only PAGE_SIZE for now, it's kinda fine
    votes = []
    comment_counts = []
    if user:
        for pp in posts:
            v = Vote.query.filter((Vote.post_id == pp.id) & (Vote.user == user.id)).first()
            comment_counts.append(Comment.query.filter_by(post_id = pp.id).count())
            if v:
                votes.append(v.value)
            else:
                votes.append(0)
    else:
        for pp in posts:
            comment_counts.append(Comment.query.filter_by(post_id = pp.id).count())
            votes.append(0)

    last_page = False
    if len(votes) < PAGE_SIZE:
        last_page = True

    comments = None
    c_p = None
    if p_id >= 0:
        comments = get_comment_dict(p_id, user)
        c_p = posts[0].message

    error = None
    if 'error' in request.args:
        error = request.args['error']
        error = None if error == '' else error

    return render_template('home.html',
                            user=user,
                            posts=zip(posts, votes, comment_counts),
                            sel=sel, page=p,
                            last_page=last_page, p_id=p_id,
                            comments=comments, error=error, c_p=c_p,
                            mit=mit)


def gen_vote_status(final, c):
    return json.dumps({'vote': final, 'count': c})

@app.route('/vote/<int:id>/<vote>')
@requires_auth()
def cast_vote(id, vote):
    my_votes = list(Vote.query.filter((Vote.post_id == id) & (Vote.user == user.id)))
    assert len(my_votes) <= 1

    post = Post.query.filter_by(id=id).first()
    if not post:
        return "Post doesn't exist."

    if vote == "upvote":
        vote_parsed = 1
    elif vote == "downvote":
        vote_parsed = -1
    else:
        return "Incorrect vote type."

    if len(my_votes) == 0:
        # Never voted
        v = Vote(post_id=id, user=user.id, value=vote_parsed)
        db.session.add(v)

        if vote_parsed > 0:
            post.upvotes += 1
        else:
            post.downvotes += 1

        db.session.commit()
        return gen_vote_status(vote_parsed, post.upvotes - post.downvotes)

    my_vote = my_votes[0]

    if my_vote.value == vote_parsed:
        # Repeating the same vote means removing the vote.
        Vote.query.filter_by(id=my_vote.id).delete()

        if vote_parsed > 0:
            # Original vote was upvote
            post.upvotes -= 1
        else:
            # Original vote was downvote
            post.downvotes -= 1

        db.session.commit()
        return gen_vote_status(0, post.upvotes - post.downvotes)

    # Else we just change the value.
    my_vote.value = vote_parsed

    if vote_parsed > 0:
        # Downvote -> Upvote
        post.downvotes -= 1
        post.upvotes += 1
    else:
        post.downvotes += 1
        post.upvotes -= 1

    db.session.commit()
    return gen_vote_status(vote_parsed, post.upvotes - post.downvotes)

@app.route('/comment/vote/<int:id>/<vote>')
@requires_auth()
def cast_comment_vote(id, vote):
    my_votes = list(CommentVote.query.filter((CommentVote.comment_id == id) & (CommentVote.user == user.id)))
    assert len(my_votes) <= 1

    post = Comment.query.filter_by(id=id).first()
    if not post:
        return "Post doesn't exist."

    if vote == "upvote":
        vote_parsed = 1
    elif vote == "downvote":
        vote_parsed = -1
    else:
        return "Incorrect vote type."

    if len(my_votes) == 0:
        # Never voted
        v = CommentVote(comment_id=id, user=user.id, value=vote_parsed)
        db.session.add(v)

        if vote_parsed > 0:
            post.upvotes += 1
        else:
            post.downvotes += 1

        db.session.commit()
        return gen_vote_status(vote_parsed, post.upvotes - post.downvotes)

    my_vote = my_votes[0]

    if my_vote.value == vote_parsed:
        # Repeating the same vote means removing the vote.
        CommentVote.query.filter_by(id=my_vote.id).delete()

        if vote_parsed > 0:
            # Original vote was upvote
            post.upvotes -= 1
        else:
            # Original vote was downvote
            post.downvotes -= 1

        db.session.commit()
        return gen_vote_status(0, post.upvotes - post.downvotes)

    # Else we just change the value.
    my_vote.value = vote_parsed

    if vote_parsed > 0:
        # Downvote -> Upvote
        post.downvotes -= 1
        post.upvotes += 1
    else:
        post.downvotes += 1
        post.upvotes -= 1

    db.session.commit()
    return gen_vote_status(vote_parsed, post.upvotes - post.downvotes)

@app.route('/app/name')
def meta_name():
    return app.CONFIG['APP_NAME']
