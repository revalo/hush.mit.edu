from confess import app
from confess.utils import *
from confess.config import *
from confess.constants import *
from confess.models.user import *
from confess.models.post import *

import os
import datetime

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

'''
Helper function that checks wether the submitted message has any issues.
Returns a bool and a string with the error message.
'''
def post_validation(message, user):
    if len(message) == 0:
        return False, "Post cannot be empty."
    if len(message) > MAX_POST_LENGTH:
        return False, "Post cannot exceed %i characters." % MAX_POST_LENGTH
    if (datetime.datetime.now() - user.last_post).total_seconds() < POST_COOLDOWN:
        return False, "Cannot post multiple times between %i seconds, you have %i seconds left." % (
                POST_COOLDOWN,
                POST_COOLDOWN - (datetime.datetime.now() - user.last_post).total_seconds()  
            )
    return True, ""

@app.route('/submit', methods=['GET', 'POST'])
@requires_auth()
def post_view():
    error = ""

    if request.method == 'POST':
        # Perform validation
        if 'message' not in request.form:
            error = "Incorrect POST data."
        else:
            message = request.form['message']
            val, e = post_validation(message, user)
            if not val:
                error = e
            else:
                # Validation successful!
                n = datetime.datetime.now()
                p = Post(message=message,
                         timestamp=n,
                         upvotes=0,
                         downvotes=0
                         )
                user.last_post = n

                db.session.add(p)
                db.session.commit()

                return redirect('/?' + str(p.id))


    # Display the submission form
    return render_template('post.html', user=user, error=error)