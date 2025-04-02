from asyncio import eager_task_factory

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
#import DummyDB
import FFEmail
from typing import List
from userinfo import User, Role, NewUserRequest, Email
from FinanceDataModels import *
from fastapi.middleware.cors import CORSMiddleware
#from DummyDB import user_table, new_user_table
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

@app.get("/events")
async def get_event_log():
    return DBA.get('Events')

@app.get("/users")
async def fetch_users():
    var = DBA.get('Users')
    return var

@app.get("/users/new_user")
async def get_new_user_requests():
    """
    Returns the list of new user requests.
    :return:
    """

    return DBA.get('User_Requests')

@app.get("/users/new_user/fetch_one")
async def get_new_user_request(email : str):
    result = DBA.get_one('User_Requests', {"email": email})
    if result is None:
        return {"Error": "User Request not found"}

    return result

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

    DBA.check_outdated_passwords()
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

@app.get("/users/login/expired_passwords")
async def get_expired_passwords():
    return DBA.get('Expired_Passwords')

@app.post("/users")
async def register_user(user: User, user_id : str):
    if type(user) is not dict:
        user = user.model_dump()
    message = DBA.insert('Users', user, user_id)
    return message

@app.post("/users/new_user")
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
    if DBA.get_one('User_Requests', {"email": user.email}) is not None:
        return {"Error": "User request already exists in system."}

    if type(user) is not dict:
        user = user.model_dump()
    message = DBA.insert('User_Requests',user, "System User Request")
    return message

@app.post("/email")
async def send_email(email: Email):
    result = FFEmail.send_email(email.recipient, email.subject, email.body)
    return {"Message": result}

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

    if type(user) is not dict:
        user = user.model_dump()

    if DBA.get_one('Users', {"user_id": user['user_id']}) is None:
        return {"Error": f"User ID {user['user_id']} not found."}

    if type(user) is not dict:
        user = user.model_dump()

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
    doc = DBA.get_one('User_Requests', {"email": email})
    if doc is None:
        return {"Error": f"User request with email {email} not found."}

    DBA.delete('User_Requests',{"email": email}, user_id)
    doc = DBA.get_one('User_Requests', {"email": email})
    if doc is None:
        return {"message": f"Successfully deleted the user request with email {email}"}
    return {"Error": f"Could not find user request with email {email}"}

@app.get("/accounts")
async def get_accounts():
    return DBA.get('Accounts')


@app.get("/accounts/balance")
async def get_account_balance(account_id: int):
    transactions = fetch_ledger_transactions(account_id)
    return sum_transaction_list(transactions)


@app.post("/accounts")
async def create_account(account : Account, user_id: str):
    if type(account) is not dict:
        account = account.model_dump()
    message = DBA.insert('Accounts', account, user_id)
    return message

@app.put("/accounts/update_one")
async def update_account_attribute(account_id : int, change: dict, admin_id: str):
    if DBA.get_one('Accounts', {"account_id": account_id}) is None:
        return {"Error" : "Account ID not found"}

    DBA.update('Accounts', {"account_id": account_id}, change, admin_id)

@app.put("/accounts/update")
async def update_account(account : Account, user_id :str):
    if type(account) is not dict:
        account = account.model_dump()

    account_id = account['account_id']
    if DBA.get_one('Accounts', {"account_id": account_id}) is None:
        return {"Error": "Account ID not found."}

    DBA.update('Accounts', {'account_id': account_id}, account, user_id)
    # print("Current Document: ")
    # print(DBA.get_one('Users', {"user_id": user['user_id']}))
    return DBA.get_one('Accounts', {"account_id": account_id})

@app.get("/accounts/get_one")
async def get_one_account(account_id: int):
    result = DBA.get_one('Accounts', {"account_id" : account_id})
    return result

@app.get("/journal")
async def get_all_journal_entries(status: ApprovedStatus = None):
    """
        Gets all the journal entries from the database. Has 4 possible parameters:
        {'status': 'approved'}
        - Returns all journal entries with the 'approved' status. This should be used for the main journal only.

        {'status': 'pending'}
        - Returns all journal entries currently pending. This should be used for the page that managers use to approve pending entries.

        {'status': 'rejected'}
        - Returns all rejected journal entries. This should be used for the page that views rejected journal entries

        None
        - No parameter given, AKA the default. This will return all journal entries regardless of status. 

        :param status:
        :return:
        """
    return fetch_journal(status=ApprovedStatus.approved)

def fetch_journal(status: ApprovedStatus = None):
    # only exists because I call get_all_journal_entries like 3 times in other api calls and using async functions is funky
    if status is None:
        return DBA.get('Journal')

    elif status == ApprovedStatus.approved:
        return DBA.get('Journal', {'status':'approved'})
    elif status == ApprovedStatus.rejected:
        return DBA.get('Journal', {'status': 'rejected'})
    elif status == ApprovedStatus.pending:
        return DBA.get('Journal', {'status': 'pending'})
    else:
        return {'Error': "Invalid status query: not 'approved', 'rejected', or 'pending'"}

@app.post("/journal")
async def post_journal_entry(entry : JournalEntry, user_id : str):
    if type(entry) is not dict:
        entry = entry.model_dump()
    transactions = entry['transactions']
    if transactions is None or len(transactions) == 0:
        return {"Error": "No transactions in journal entry"}

    journals = fetch_journal(status=ApprovedStatus.approved)

    total_trans_count = 0

    if journals is not None:
        for jentry in journals:
            total_trans_count += len(jentry['transactions']) # gets the total number of transaction lines in the entire journal

    balance = sum_transaction_list(transactions)

    for trans in transactions:
        total_trans_count += 1
        journal_page = total_trans_count % JOURNAL_PAGE_LENGTH

        trans['journal_page'] = f"J{journal_page}"

    if balance != 0:
        return {"Error": "Journal Entry is not balanced. Check your debits and credits again. "}

    entry['date'] = entry['transactions'][0]['date']

    message = DBA.insert('Journal', entry, user_id)
    return message

def sum_transaction_list(transactions: List[Transaction]):
    balance = 0
    if transactions is not None:
        for trans in transactions:
            if trans['side'] == "debit":
                balance += trans['balance']
            elif trans['side'] == "credit":
                balance -= trans['balance']

    return balance


@app.get("/ledger/transactions")
async def get_ledger_transactions(account_id: int):
    return fetch_ledger_transactions(account_id)

def fetch_ledger_transactions(account_id: int):
    entries = fetch_journal(status=ApprovedStatus.approved)

    if entries is None:
        return {}  # there are no entries yet, so it returns empty but valid data so it does not cause an error

    trans_list = []
    for entry in entries:
        entry_transactions = entry['transactions']
        for trans in entry_transactions:
            if trans['account_id'] == account_id:
                trans_list.append(trans)

    return trans_list
