from pymongo import MongoClient


class Mongo:
    def __init__(self, uri):
        self._client = MongoClient(uri, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
        self._db = self._client.get_database()

    @property
    def db(self):
        return self._db

