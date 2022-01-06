from pymongo import MongoClient
DATABASE_NAME = 'mydatabase'
# DATABASE_NAME = 'IMS-DB'
# COLLECTION_NAME = 'IMS-DB'
# DATABASE_HOST = 'ISE-IntNet-W36'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '27017'
# USERNAME = 'admin'
# PASSWORD = 'mongo1234'


def get_db_handle():
    client = MongoClient(host=DATABASE_HOST,
                         port=int(DATABASE_PORT),
                         # username=username,
                         # password=password
                        )
    db_handle = client[DATABASE_NAME]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]