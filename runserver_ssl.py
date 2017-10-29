## Legacy code, needs to be changed for gunicorn

from confess import app
from confess import socketio
from confess.config import PORT, DEBUG

if __name__ == '__main__':
    socketio.run(app,
        host='0.0.0.0',
        port=443,
        keyfile='./confess/private/c.mit.edu.key',
        certfile='./confess/private/c_mit_edu_cert.cer',
        debug=DEBUG
    )
