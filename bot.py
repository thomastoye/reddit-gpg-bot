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
import persistence

class RedditGpgBot:
    user_agent = '/r/GPGpractice practicer'
    subreddit = 'GPGpractice' 

    def __init__(self):
        print('reddit GPG bot is starting up')
        self.agent = praw.Reddit(self.user_agent)
        self.agent.login(config.REDDIT_USER, config.REDDIT_PASS)
        
        self.persistence = persistence.Persistence(config.MONGO_URI)

        self.gpg = gnupg.GPG(homedir = 'gpg-homedir')
        
        self.main_loop()

    def  main_loop(self):
        while True:
            submissions = self.agent.get_subreddit(self.subreddit).get_hot(limit = 10000)
            
            for thread in submissions:
                if not self.thread_already_handled(thread):
                    self.handle_thread(thread)
                else:
                    print('thread %s already handled, skipping' % thread.id)

            break

    def thread_already_handled(self, thread):
        return self.persistence.is_thread_in_db(thread.id)

    def format_gpg_message(self, thread):
        return '\n' + '\n'.join([' ' * 4 + line for line in str(enc).split('\n')])

    def reply_to_thread(self, thread_id, msg):
        pass

    def handle_thread(self, thread):
        public_key = self.extract_public_key(thread.selftext)

        if public_key:
            res = self.gpg.import_keys(public_key)
            print('Tried to import a key, result: %s (counts: %s)' % (res.summary(), res.counts))
            if res.counts['count'] is 0:
                print('Seems like I couldn\'t import the key. stderr of gpg: %s' % res.stderr)
                print('\nThe key in this case was:\n***\n%s\n\n***' % public_key)
                self.persistence.register_public_key_found(thread.id, public_key, res.stderr, res.summary(), False)
            else:
                self.persistence.register_public_key_found(thread.id, public_key, res.stderr, res.summary(), True)
            return True
        else:
            self.persistence.register_no_public_key_found(thread.id)
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


