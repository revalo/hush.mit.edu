import os
import requests
import cPickle as pickle

from confess.config import *
from confess.models.post import *
from confess.models.facebook_post import *

from apscheduler.schedulers.background import BackgroundScheduler

print "Scheduler was enabled."

def post_to_facebook(message, link):
    url = "https://graph.facebook.com/v2.11/{page_id}/feed".format(page_id=FACEBOOK_PAGE_ID)
    r = requests.post(url, data={'message': message, 'access_token': FACEBOOK_TOKEN, 'link': link})
    j = r.json()

    if "error" in j:
        print j

    return j

sched = BackgroundScheduler()
sched.start()

@sched.scheduled_job('interval', id='facebook_worker', seconds=FACEBOOK_WORKER_INTERVAL)
def facebook_post_worker():
    # Acquire table lock
    db.session.begin_nested()
    db.session.execute('LOCK TABLE facebook_post IN ACCESS EXCLUSIVE MODE;')

    # Check if there is new content
    hot = db.session.query(Post).order_by(Post.hn_score.desc()).limit(FACEBOOK_TOP_N)
    for item in hot:
        existing = FacebookPost.query.filter_by(post_id=item.id).first()
        if not existing:
            try:
                message = "#{id} {message}".format(id=item.id,
                                                   message=item.message)
                if not "error" in post_to_facebook(message, 'https://hush.mit.edu' + '/?' + str(item.id)):
                    f = FacebookPost(post_id=item.id)
                    db.session.add(f)
            except Exception as e:
                print e
                pass

    # Release table lock
    db.session.commit()
    db.session.commit()