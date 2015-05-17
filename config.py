import os

REDDIT_USER = os.environ.get('REDDIT_USERNAME')
REDDIT_PASS = os.environ.get('REDDIT_PASSWORD')

BOT_PRIVATE_KEY = os.environ.get('BOT_PRIVATE_KEY')

MONGO_URI = os.environ.get('MONGOLAB_URI')

if not BOT_PRIVATE_KEY:
    print('error: you must provide a private key for the bot (BOT_PRIVATE_KEY)')
    sys.exit(1)

if not MONGO_URI:
    print("error: you must provide a mongodb URI as an environment variable (MONGOLAB_URI)")
    sys.exit(1)

if not REDDIT_USER:
    print('error: you must provide a reddit username as an environment variable (REDDIT_USERNAME)')
    sys.exit(1)

if not REDDIT_PASS:
    print('error: you must provide a reddit password as an environment variable (REDDIT_PASSWORD)')
    sys.exit(1)

