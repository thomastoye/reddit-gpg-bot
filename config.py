import os

REDDIT_USER = os.environ.get('REDDIT_USERNAME')
REDDIT_PASS = os.environ.get('REDDIT_PASSWORD')

MONGO_URI = os.environ.get('MONGOLAB_URI')

if not MONGO_URI:
    print("error: you must provide a mongodb URI as an environment variable (MONGOLAB_URI)")
    sys.exit(1)

if not REDDIT_USER:
    print('error: you must provide a reddit username as an environment variable (REDDIT_USERNAME)')
    sys.exit(1)

if not REDDIT_PASS:
    print('error: you must provide a reddit password as an environment variable (REDDIT_PASSWORD)')

