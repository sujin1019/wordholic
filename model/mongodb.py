import pymongo
from controllers.db_controller import mongodb_access_info

USERNAME = mongodb_access_info()['username']
PASSWORD = mongodb_access_info()['password']
MONGO_HOST = mongodb_access_info()['host']


def conn_mongodb():
    try:
        MONGO_CONN = pymongo.MongoClient(('mongodb://{}:{}@{}').format(USERNAME, PASSWORD, MONGO_HOST))
        MONGO_CONN.admin.command('ismaster')
        word_collection = MONGO_CONN.word_db.word_collection
    except:
        MONGO_CONN = pymongo.MongoClient(('mongodb://{}:{}@{}').format(USERNAME, PASSWORD, MONGO_HOST))
        word_collection = MONGO_CONN.word_db.word_collection

    return word_collection