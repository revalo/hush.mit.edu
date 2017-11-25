from confess import app
from confess.utils import *
from confess.config import *
from confess.constants import *
from confess.models.user import *
from confess.models.post import *

import os
import random
import datetime
import humanize
import StringIO

from confess.image_utils import *

from PIL import ImageFont
# Load font into memory
font = ImageFont.truetype('confess/static/SourceCodePro-Regular.ttf', 18)

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template,
    send_file
)

def human_delta(seconds):
    return humanize.naturaltime(datetime.timedelta(seconds=seconds)).replace(' ago', '')

'''
Helper function that checks wether the submitted message has any issues.
Returns a bool and a string with the error message.
'''
def post_validation(message):
    if len(message) == 0:
        return False, "Post cannot be empty."
    if len(message) > MAX_POST_LENGTH:
        return False, "Post cannot exceed %i characters." % MAX_POST_LENGTH
    return True, ""

@app.route('/submit', methods=['GET', 'POST'])
@get_user()
def post_view():
    error = ""

    mit = is_mit(request)

    if request.method == 'POST':
        if not mit and not user:
            error = "You need to be connected to the MIT Network or login to post :/"
        elif not validate_recaptcha(request.form):
            error = "Incorrect CAPTCHA."
        # Perform validation
        elif 'message' not in request.form:
            error = "Incorrect POST data."
        else:
            message = request.form['message']
            val, e = post_validation(message)
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

                db.session.add(p)
                db.session.commit()

                return redirect('/?' + str(p.id))


    # Display the submission form
    return render_template('post.html', user=user,
                                        error=error,
                                        cooldown_text=human_delta(POST_COOLDOWN),
                                        mit=mit)


@app.route('/post/<int:id>/image')
def post_image(id):
    p = Post.query.filter_by(id=id).first()
    if not p:
        return "Post doesn't exist", 400

    width, height = (1200, 630) # From facebook
    message = p.message

    image = ImageText((width, height), background="#146eff")
    image.write_text_box((0, 0), message, box_width=width, font_filename='confess/static/SourceCodePro-Regular.ttf',
                          font_size=32, color=(255, 255, 255), place="center")

    # From https://stackoverflow.com/a/10170635
    img_io = StringIO.StringIO()
    image.image.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')