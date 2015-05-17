
import pymongo

class Persistance:
    def __init__(self, mongo_uri):
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client.get_default_database()

    def register_no_public_key_found(self, thread_id):
        self.mongo_db['threads'].insert({'thread_id': thread_id, 'status': 'No key found'})

    def register_public_key_found(self, thread_id, public_key, stderr, summary, gpg_import_was_successful = True):
        status = 'success' if gpg_import_was_successful else 'error'
        self.mongo_db['threads'].insert({'thread_id': thread_id, 'public_key': public_key, 'gpg_import': {'status': status, 'stderr': stderr, 'summary': summary}})
        

