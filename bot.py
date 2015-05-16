#!/usr/bin/env python3

import praw
import gnupg
import time
import re
import public_key_providers
import config
import pymongo
import os
import sys

class RedditGpgBot:
    user_agent = '/r/GPGpractice practicer'
    subreddit = 'GPGpractice' 

    def __init__(self):
        print('reddit GPG bot is starting up')
        self.agent = praw.Reddit(self.user_agent)
        self.agent.login(config.REDDIT_USER, config.REDDIT_PASS)
        
        self.gpg = gnupg.GPG(homedir = 'gpg-homedir')
        
        self.mongo_client = pymongo.MongoClient(config.MONGO_URI)
        self.mongo_db = self.mongo_client.get_default_database()

        self.main_loop()

    def  main_loop(self):
        while True:
            submissions = self.agent.get_subreddit(self.subreddit).get_hot(limit = 10000)
            t = [(thread, self.handle_thread(thread)) for thread in submissions]

            break

    def thread_already_handled():
        # make call to mongodb, etc.
        pass

    def handle_thread(self, thread):
        public_key = self.extract_public_key(thread.selftext)

        if public_key:
            res = self.gpg.import_keys(public_key)
            print('Tried to import a key, result: %s' % res.summary())
            if res.counts['count'] is 0:
                print('Seems like I couldn\'t import the key. stderr of gpg: %s' % res.stderr)
                print('\nThe key in this case was:\n***\n%s\n\n***' % public_key)
                self.mongo_db['threads'].insert({'thread_id': thread.id, 'public_key': public_key, 'gpg_import': {'status': 'error', 'stderr': res.stderr, 'summary': res.summary()}})
            else:
                self.mongo_db['threads'].insert({'thread_id': thread.id, 'public_key': public_key, 'gpg_import': {'status': 'success', 'stderr': res.stderr, 'summary': res.summary()}})
            return True
        else:
            self.mongo_db['threads'].insert({'thread_id': thread.id, 'status': 'No key found'})
            print('No key found in %s' % thread.url)
            return False

    """ Iterate over all providers, return as soon as one succeeds """
    def extract_public_key(self, text):
        for provider in public_key_providers.all_providers:
            res = provider(text)
            if res:
                return res

        return None

if __name__ == '__main__':
    RedditGpgBot()


