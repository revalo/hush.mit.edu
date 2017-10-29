from confess import app
from confess.config import PORT, DEBUG

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )