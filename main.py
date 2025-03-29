from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
import DummyDB
import FFEmail
from typing import List
from userinfo import User, Role, NewUserRequest, Email
from fastapi.middleware.cors import CORSMiddleware
from DummyDB import user_table, new_user_table
import DatabaseAccess as DBA

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# adding a comment here

class Request(BaseModel):
    type: str = None
    req: str = None

@app.get("/")
async def root():
    return {"Greeting": "You have accessed the root of the FastFinance API."}

#the primary way the app will get user data to display on the screen
@app.get("/users")
async def fetch_users():
    var = DBA.get('Users')
    return var

@app.get("users/new_user")
async def get_new_user_requests():
    """
    Returns the list of new user requests.
    :return:
    """

    return DBA.get('User_Requests')

@app.get("/users/login")
async def login(user_id : str, hashed_pass : str):
    """

    Takes a username string and hashed_password string and attempts to log in.

    it will return a JSON with one field: "message", which includes the role of the user and " Login Successful", eg:
    {"message": "Accountant Login Successful"}
    {"message": "Manager Login Successful"}
    {"message": "Admin Login Successful"}

    depending on the user's role.

    :param user_id:
    :param hashed_pass:
    :return:
    """

    #DummyDB.check_outdated_passwords()
    # the above line is to check every current password in the system if they are about to expire, and send an email if so.
    # this happens during every login request because at least one user logging in is a very frequent and consistent action

    user = DBA.get_one('Users', {"user_id": user_id}) # user is a dict

    if user is None:
        return {"Error" : "Incorrect Username or Password"}
    failed_attempts = user['failed_attempts']
    if user['hashed_pass'] == hashed_pass:
        #if the failed attempts are greater than zero, reset it back to zero on a successful login. This is to avoid update log spam every time someone logs in
        if failed_attempts > 0:
            DBA.update('Users', {'user_id': user['user_id']}, {'failed_attempts': 0},"System Login")

        if user['status'] is False:
            return {"Error": "Account Suspended"}
        if user['role'] == Role.admin:
            return {"message": "admin"}
        elif user['role'] == Role.manager:
            return {"message": "manager"}
        else:
            return {"message": "accountant"}
    else:
        DBA.update('Users', {'user_id' : user['user_id']},{'failed_attempts': failed_attempts + 1}, "System Login")
        return {"Error": "Incorrect Username or Password"}

@app.get("/users/login/forgot_password")
async def forgot_pass(user_id : str):
    """
    Takes the ID of a user and returns a list with their 3 security passwords

    function defined by the path: /users/update with the "put" parameter
    :param user_id:
    :return:
    """
    user = DBA.get_one('Users', {"user_id": user_id})
    if user is None:
        return {"Error" : "User not found"}

    user_answers = user['security_answers']
    return user_answers

# The primary way the admin will add a user to the system.
@app.post("/users")
async def register_user(user: User, user_id : str):
    message = DBA.insert('Users', user, user_id)
    return message
#weird shit going on tonight

@app.post("users/new_user")
async def new_user(user: NewUserRequest):
    """
    Function to create a "new user" request in the system.
    The format for a new user request JSON looks like:
    {
        "first_name": <first name string>
        "last_name": <last name string>
        "email": <email address string>
        "dob": <string in format dd/mm/yyyy>
    }
    Admins will see new user requests on their client.
    To create a new user in the database, use the post:"/users" api call.

    :param user:
    :return:
    """
    message = DBA.insert('User_Requests',user, "System User Request")
    return message

@app.post("/email")
async def send_email(email: Email):
    result = FFEmail.send_email(email.recipient, email.subject, email.body)
    return {"Message": result}

# the primary way an admin will update user info.
# this includes changing personal info about the user and activating or deactivating them
@app.put("/users/update")
async def update_user(user: User, user_id: str):
    """
    Takes in an entire user document and the id of the admin making the change.

    The user document must include every field, including the ones that are not changed. It simply replaces
    the document in the database with the new one being passed in. This allows multiple changes to happen with
    one update call.

    If the user is not found, it returns and error.
    If it is successful, it gets the changed document from the database and returns it.

    :param user:
    :param user_id:
    :return:
    """

    if DBA.get_one('Users', {"user_id": user['user_id']}) is None:
        return {"Error": f"User ID {user['user_id']} not found."}

    DBA.update('Users', {'user_id' : user['user_id']}, user, "System Login")
    #print("Current Document: ")
    #print(DBA.get_one('Users', {"user_id": user['user_id']}))
    return DBA.get_one('Users', {"user_id": user['user_id']})


@app.put("/users/update_one")
async def update_user_attribute (user_id: str, change: dict, admin_id : str):
    """
    Like update, but instead of taking the entire user object, it only takes the user_id of the user to change
    and the single field to be changed. Takes the ID of the admin making the change as usual.

    :param user_id:
    :param change:
    :param admin_id:
    :return:
    """

    if DBA.get_one('Users', {"user_id": user_id}) is None:
        return {"Error": "User ID not found."}

    DBA.update('Users', {'user_id' : user_id}, change, admin_id)

    return DBA.get_one('Users', {"user_id": user_id})


@app.delete("/users/new_user")
async def delete_new_user_request(email: str, user_id : str):
    DBA.delete('User_Requests',{"email": email}, user_id)
    doc = DBA.get_one('User_Requests', {"email": email})
    if doc is None:
        return {"message": f"Successfully deleted the user request with email {email}"}
    return {"Error": f"Could not find user request with email {email}"}
