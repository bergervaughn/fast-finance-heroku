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
    print(var)
    return var

@app.get("users/new_user")
async def get_new_user_requests():
    """
    Returns the list of new user requests.
    :return:
    """
    return {"message": "Unfinished function"}

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
            DBA.update('Users', {'user_id': user['user_id']}, {'$set': {'failed_attempts': 0}},"System Login")


        if user['status'] is False:
            return {"Error": "Account Suspended"}
        if user['role'] == Role.admin:
            return {"message": "admin"}
        elif user['role'] == Role.manager:
            return {"message": "manager"}
        else:
            return {"message": "accountant"}
    else:
        DBA.update('Users', {'user_id' : user['user_id']},{'$set': {'failed_attempts': failed_attempts + 1}}, "System Login")
        return {"Error": "Incorrect Username or Password"}

@app.get("/users/'login/forgot_password")
async def forgot_pass(user_id : str, answers: List[str], hashed_pass : str):
    """
    Takes 5 strings: the user ID, the three security answer strings, and the new password string.

    If successful, it will update the system with the new password
    If not, it will return one of a few errors, depending on whether the username or one of the security questions was wrong

    function defined by the path: /users/update with the "put" parameter
    :param hashed_pass:
    :param user_id:
    :param answers:
    :return:
    """
    user = DBA.get_one('Users', {"user_id": user_id})
    user_answers = user['security_answers']

    if user_answers == answers:
        DBA.update('Users', {'user_id': user['user_id']}, {'$set': {'hashed_pass' : hashed_pass}}, "System Password Update")
        return {"Message" : "Password Updated Successfully"}

    return {"Error": "Security question incorrect"}

# The primary way the admin will add a user to the system.
@app.post("/users")
async def register_user(user: User):
    user_table.append(user)
    return {"id": user.user_id}
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
    new_user_table.append(user)
    return {"email": user.email}

@app.post("/email")
async def send_email(email: Email):
    result = FFEmail.send_email(email.recipient, email.subject, email.body)
    return {"Message": result}

# the primary way an admin will update user info.
# this includes changing personal info about the user and activating or deactivating them
@app.put("/users/update")
async def update_user(user: User):
    for u in user_table:
        if user.user_id == u.id:
            if user.hashed_pass is not None:
                for old_pass in u.past_passwords:
                    if user.hashed_pass == old_pass:
                        raise HTTPException(405, {"Error": "New Password cannot be an old password."})
                u.hashed_pass = user.hashed_pass
                u.password_expiration = date.today() + timedelta(days=90)
            if user.email is not None:
                u.email = user.email
            if user.status is not None:
                u.status = user.status
            if user.first_name is not None:
                u.first_name = user.first_name
            if user.last_name is not None:
                u.last_name = user.last_name
            return {f"User with ID {user.id} updated successfully."}
    raise HTTPException(
        status_code=404,
        detail=f"User with ID: {user.user_id} does not exist."
    )


#
# @app.delete("/users/new_user")
# async def delete_new_user_request(email: str):
#     for user in new_user_table:
#         if email == user:
#             new_user_table.remove(user)
#             return {"Message": "New User Request successfully deleted."}
#
#     raise HTTPException(404, "User not found.")

