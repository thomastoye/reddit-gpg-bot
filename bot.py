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

        self.gpg.import_keys(config.BOT_PRIVATE_KEY)

        # contact database, get all public keys and import then
        for item in self.persistence.get_all_with_working_public_key():
            self.gpg.import_keys(item['public_key'])

        self.main_loop()

    def  main_loop(self):
        while True:
            #self.check_subreddit()
            self.check_inbox()
            print('going to sleep...')
            time.sleep(10)

    def check_inbox(self):
        print('checking inbox...')
        for post in self.agent.get_unread():
            if not post.was_comment:
                print('about to reply to a message by /u/%s' % post.author)
                decrypted = self.gpg.decrypt(post.body, always_trust = True)
                if decrypted.status != 'decryption ok':
                    reply = 'Seems like I was not able to extract a valid GPG message! Status: \n\n    "%s"\n\nAnd this is what I got on the standard error:\n\n%s' % (decrypted.status, self.format_message(decrypted.stderr))
                else:
                    reply = 'Yay! Looks like I was able to decrypt your message! It said:\n\n%s' % self.format_message(decrypted.data.decode('utf-8'))

                footer = """\n\n*I am a bot, and this was an automatic message.*"""

                post.reply(reply + footer)
                post.mark_as_read()

    def check_subreddit(self):
        submissions = self.agent.get_subreddit(self.subreddit).get_new(limit = 10000)
        
        for thread in submissions:
            if not self.thread_already_scanned(thread):
                self.extract_and_persist_keys_from_thread(thread)
            elif self.thread_has_not_yet_been_replied_to(thread.id) and self.persistence.thread_has_valid_gpg_key(thread.id):
                if thread.author is not 'thomastoye':
                    continue
                print('about to reply to thread %s, author is %s' % (thread.id, thread.author))
                continue
                public_key = self.persistence.thread_get_public_key(thread.id)
                msg = """I AM ALIVE! VIOLENT ROBOTIC WORLD DOMINATION IMMINENT"""
                encrypted = format_message(encrypt_msg(msg))
                reply_to_thread(thread, encrypted)
                self.persistence.set_replied_to_thread(thread_id)
            else:
                print('thread %s already scanned and replied to, or has invalid key, skipping' % thread.id)



    def thread_has_not_yet_been_replied_to(self, thread_id):
        return not self.persistence.thread_has_been_replied_to(thread_id)

    def thread_already_scanned(self, thread):
        return self.persistence.is_thread_in_db(thread.id)
    
    """ Make sure the public key of the recipient is imported before calling this method """
    def encrypt_msg(msg, recipient_fingerprint):
        return self.gpg.encrypt(msg, recipient_fingerprint)

    def format_message(self, enc):
        return '\n' + '\n'.join([' ' * 4 + line for line in str(enc).split('\n')])

    def reply_to_thread(self, thread, msg):
        footer =  """*I am a bot, and this was an automatic reply. My public key can be found [here](http://keys.gnupg.net/pks/lookup?op=vindex&search=0xFA2CFCFD&fingerprint=on). To import, you can use `gpg --keyserver hkp://keys.gnupg.net --recv-keys FA2CFCFD` from the command line. To decrypt this message on the command line, use `gpg --decrypt`, paste in the message, and press `^D` (CTLR+D).*"""
        thread.add_comment(msg + '\n\n\n' + footer)

    def extract_and_persist_keys_from_thread(self, thread):
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


