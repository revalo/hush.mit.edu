# Server runnning port.
PORT = 80

# Postgres SQL Connection String.
DB_URI = 'postgresql://username:password@localhost/confess'

# Full domain name.
DOMAIN = 'http://localhost'

# Random Secret for JWTs.
SECRET = 'some_secret'

# Name
APP_NAME = 'hush.mit.edu'

# Debug
DEBUG = True

# Cooldown
POST_COOLDOWN = 86400 # 1 day

# Maxmium post message length
MAX_POST_LENGTH = 3000

# Post cutoff
CUTOFF_POST_LENGTH = 400

# Page size
PAGE_SIZE = 20