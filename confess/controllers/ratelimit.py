from confess import app
from confess.utils import *
from confess.constants import *
from confess.config import *
from confess.models.ratelimit import *

import datetime

try:
    # Trunctate table on start, reset cooldowns.
    RateLimit.query.delete()
    db.session.commit()
except Exception as e:
    print "Ignoring RateLimit truncate exception."


def is_ratelimited(request):
    ip = get_ip(request)
    n = datetime.datetime.now()

    entry = RateLimit.query.filter_by(ip=ip).first()
    if not entry:
        r = RateLimit(ip=ip, last_request=n)
        db.session.add(r)
        db.session.commit()
        return False

    secs = (n - entry.last_request).total_seconds()
    if secs < POST_COOLDOWN:
        return True

    entry.last_request = n
    db.session.commit()

    return False