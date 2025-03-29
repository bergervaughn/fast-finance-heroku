from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId

uri = "mongodb+srv://FastFinancesAdmin:fastfin13@fastfinances.p3wik.mongodb.net/?retryWrites=true&w=majority&appName=FastFinances"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error while pinging:", e)

db = client['FastFinances']

def get_one(collection, query):
    collection = db[collection]
    document = collection.find_one(query)
    return document

# #sample usage
# collection = db['Users']
# query = {'_id': 'user1234'}
# document = get_one(collection, query)
# print(document)

def get(collection):
    collection = db[collection]
    cursor = collection.find()
    return cursor.to_list()

# #sample usage
# collection = db['Accounts']
# query = query = {'name': 'John Doe'}
# document = get(collection, query)
# print(document)

def error(error_description):
    collection = db['Errors']
    now = datetime.now()
    error_date = now.strftime("%Y-%m-%d")
    error_time = now.strftime("%H:%M:%S")
    error_doc = {
        'error_id' : ObjectId(),
        "error_description": error_description,
        "date": error_date,
        "time": error_time
    }
    collection.insert_one(error_doc)
    return


def event(original, updated, user_id):
    collection = db['Events']
    now = datetime.now()
    event_date = now.strftime("%Y-%m-%d")
    event_time = now.strftime("%H:%M:%S")
    event_doc = {
        'event_id' : ObjectId(),
        'from' : original,
        'to' : updated,
        "user_id": user_id,
        "date": event_date,
        "time": event_time
    }
    collection.insert_one(event_doc)
    return


def update(collection, query, update, user_id):
    original = collection.find_one(query)
    collection.update_one(query, update)
    updated = collection.find_one(query)
    if original == updated:
        error('Attempted to change a document from a state to an identical state')
        return
    event(original, updated, user_id)
    return

#sample usage of event is found below insert

def insert(collection, document, user_id):
    if collection.find_one({'_id': document['_id']}):
        error('Attempted to insert a document when a document with an identical id exists')
        return
    collection.insert_one(document)
    event(None, document, user_id)
    return

# #sample usage THIS MUST FIT FORMAT OF WHERE YOU ARE INSERTING
# test_doc = {
#     '_id': 'user1234',
#     'hashed_pass': 'hashed_password_example',
#     'past_passwords': ['hashed_password_old1', 'hashed_password_old2'],
#     'email': 'johndoe@example.com',
#     'status': True,
#     'role': 'user',
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'dob': '1990-05-15',
#     'failed_attempts': 0,
#     'password_expiration': '2025-05-15',
#     'security_answers': ['answer1', 'answer2', 'answer3'],
#     'suspension_start_date': '',
#     'suspension_end_date': ''
# }
# collection = db['Users']
# user_id = 'user1234'
# insert(collection, test_doc, user_id)
#
#
# #sample usage of EVENT
# collection = db['Users']
# query = {'_id': 'user1234'}
# change = {'$set': {'first_name': 'James'}}
# user_id = 'user1234'
# update(collection, query, change, user_id)