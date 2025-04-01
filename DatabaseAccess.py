from gc import collect

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId

import FFEmail

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
    document = collection.find_one(query, {'_id': False})
    return document

# #sample usage
# collection = db['Users']
# query = {'_id': 'user1234'}
# document = get_one(collection, query)
# print(document)

def get(collection):
    collection = db[collection]
    cursor = collection.find({},{'_id': False})
    return cursor.to_list()

# #sample usage
# collection = db['Accounts']
# query = query = {'name': 'John Doe'}
# document = get(collection, query)
# print(document)

def error(error_id : int, error_description : str):
    collection = db['Errors']
    now = datetime.now()
    error_date = now.strftime("%Y-%m-%d")
    error_time = now.strftime("%H:%M:%S")
    error_doc = {
        'error_id' : error_id,
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
    if original is not None:
        if '_id' in original:
            del original['_id']
    if updated is not None:
        if '_id' in updated:
            del updated['_id']
    event_doc = {
        'event_id' : str(ObjectId()),
        'from' : original,
        'to' : updated,
        "user_id": user_id,
        "date": event_date,
        "time": event_time
    }
    collection.insert_one(event_doc)
    return


def update(collection, query, update, user_id):
    collection = db[collection]
    original = collection.find_one(query,{'_id': False})
    collection.update_one(query, {'$set': update})
    updated = collection.find_one(query,{'_id': False})
    if original == updated:
        #error('Attempted to change a document from a state to an identical state')
        return {'Error': 'Attempted to change a document from a state to an identical state'}
    event(original, updated, user_id)
    return

#sample usage of event is found below insert

def insert(collection, document, user_id):
    collection = db[collection]
    collection.insert_one(document)
    event(None, document, user_id)
    return {"message" : "Document successfully inserted"}

def delete(collection, query, user_id):
    deleted = get_one(collection, query)
    collection = db[collection]
    collection.delete_one(query)
    event(deleted, None, user_id)

def check_outdated_passwords():
    users = get('Users')
    now = datetime.now().date()
    for user in users:
        user_id = user['user_id']
        status = user['status']
        password_expiration = user['password_expiration']
        expiration_date = datetime.strptime(password_expiration, '%Y-%m-%d').date()
        delta = expiration_date - now
        if delta.days <= 0 and status == True:  # checks to make sure they are not already suspended so it doesn't resuspend someone everytime this is checked.

            print(f'User {user_id} has an expired password.')

            doc = {
                'user_id': user_id  ,
                'email' : user['email'],
                'password_expiration': user['password_expiration']
            }
            if get_one('Expired_Passwords', user_id) is None:  # check to ensure no duplicated are added to the database
                insert('Expired_Passwords', doc, "System Password Check")
                print(f"User {user_id} has been added to the expired password collection.")

            update('Users', {'user_id': user_id}, {"status": False}, "System Password Check")  # suspends them
            print(f"User {user_id} has been suspended.")

        result = get_one('Expired_password', {'user_id': user_id})
        if delta.days > 0 and result is not None:
            print(f'User {user_id} no longer has an expired password.')

            delete('Expired_Passwords', {'user_id': user_id}, "System Password Check")
            print(f"User {user_id} has been removed from the Expired Password collection.")

            #update('Users', {'user_id': user_id}, {"status": True}, "System Password Check")  # removes the suspension
            #print(f'User {user_id} has been unsuspended.')
    return

# def remove_id_recursive():
#     collection = db['Events']
#     result = collection.update_many(
#         {"_id": {"$type": "objectId"}},  # Filter to find documents with event_id as ObjectId
#         [
#             {"$set": {"event_id": {"$toString": "$event_id"}}}  # Convert ObjectId to string
#         ]
#     )
#     return result
#
#
def remove_referenced_object_ids():
    collection = db['Events']

    # Iterate over all documents in the collection
    for event in collection.find():
        # Prepare an update document to remove _id from referenced objects
        update_fields = {}

        # Loop through each field in the event document
        for field, value in event.items():
            if isinstance(value, dict) and '_id' in value and isinstance(value['_id'], ObjectId):
                # If the value is a dict and contains an ObjectId in _id, remove the _id
                update_fields[f"{field}._id"] = None  # Removing the _id field from the referenced object

        if update_fields:
            # Perform the update only if there are _id fields to remove
            result = collection.update_one(
                {'_id': event['_id']},  # Find the document by its _id
                {'$unset': update_fields}  # Use $unset to remove _id fields in referenced objects
            )
            print(f"Updated event with _id {event['_id']}: {result.modified_count} fields modified.")
        else:
            print(f"No referenced _id to remove in event with _id {event['_id']}.")

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