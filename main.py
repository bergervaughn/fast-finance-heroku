import base64
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile, Response
from datetime import datetime
from dateutil.relativedelta import relativedelta
import FFEmail

from userinfo import User, Role, NewUserRequest, Email
from FinanceDataModels import *
from fastapi.middleware.cors import CORSMiddleware
import DatabaseAccess as DBA

app = FastAPI()

origins = ["*"]
# API Link: https://fast-finance-e250d1a7d65a.herokuapp.com/
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

@app.put("/user/login/reset_password")
async def reset_password(user_id: str, change: dict, admin_id : str):
    user = DBA.get_one('Users', {"user_id": user_id})
    if user is None:
        return {"Error": "User ID not found."}

    past_passwords = user['past_passwords'] # should return a list
    current_pass = user['hashed_pass']

    past_passwords.append(current_pass)

    current_date = datetime.now()
    date_3_months_later = current_date + relativedelta(months=+3)
    password_expiration = date_3_months_later.strftime("%Y-%m-%d")

    change['past_passwords'] = past_passwords
    change['password_expiration'] = password_expiration

    DBA.update('Users', {'user_id': user_id, }, change, admin_id)

@app.post("/users")
async def register_user(user: User, user_id : str):
    if type(user) is not dict:
        user = user.model_dump()

    if DBA.get_one("Users", {'user_id': user['user_id']}) is not None:
        return {"Error": "User already exists in system."}

    current_date = datetime.now()
    date_3_months_later = current_date + relativedelta(months=+3)
    user['password_expiration'] = date_3_months_later.strftime("%Y-%m-%d")

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

    DBA.update('Users', {'user_id' : user['user_id']}, user, user_id)
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
    accounts = DBA.get('Accounts')

    for account in accounts:
        account_id = account['account_id']
        bal = sum_transaction_list(fetch_ledger_transactions(account_id))
        account['balance'] = bal

    return accounts


@app.get("/accounts/balances")
async def get_account_balances():
    accounts = DBA.get('Accounts', {})
    balances = []
    for account in accounts:
        account_id = account['account_id']
        bal = sum_transaction_list(fetch_ledger_transactions(account_id))
        balances.append(bal)

    return balances

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
        Gets all the journal entries from the database.
        Has 4 possible parameters:
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
    return fetch_journal(status=status)

@app.get("/journal/get_one")
async def get_one_journal(journal_id: str):
    """
    Returns the info for just one journal.
    :param journal_id:
    :return:
    """
    result = DBA.get_one('Journal', {'journal_id': journal_id})

    return result

def fetch_journal(status: ApprovedStatus = None):
    # only exists because I call get_all_journal_entries like 3 times in other api calls and using async functions is funky

    if status is None:
        return DBA.get('Journal')

    if status == ApprovedStatus.approved or status == ApprovedStatus.pending or status == ApprovedStatus.rejected:
        status = status.value
        return DBA.get('Journal', {'approved_status': status})

    # if status == ApprovedStatus.approved:
    #     return DBA.get('Journal', {'approved_status':'approved'})
    # elif status == ApprovedStatus.rejected:
    #     return DBA.get('Journal', {'approved_status': 'rejected'})
    # elif status == ApprovedStatus.pending:
    #     return DBA.get('Journal', {'approved_status': 'pending'})
    # else:
    #     return {'Error': "Invalid status query: not 'approved', 'rejected', or 'pending'"}

@app.post("/journal")
async def post_journal_entry(entry : JournalEntry, user_id : str):
    if type(entry) is not dict:
        entry = entry.model_dump()


    transactions = entry['transactions']
    if transactions is None or len(transactions) == 0:
        return {"Error": "No transactions in journal entry"}

    if len(transactions) == 1:
        return {"Error": "Journal entry cannot have only one transaction"}

    status = entry['approved_status']
    if status != 'approved' or status != 'pending':
        entry['approved_status'] = 'pending'
    if status == 'approved':
        assign_journal_pages(entry)



    balance = sum_transaction_list(transactions)

    if balance != 0:
        return {"Error": "Journal Entry is not balanced. Check your debits and credits again."}


    date = entry['transactions'][0]['date']
    entry['date'] = date

    if "description" not in entry:
        entry["description"] = ""

    entry['comment'] = ""

    transaction1 = "".join(transactions[0]['account_name'].split()) #gets affected account name without whitespace
    transaction2 = "".join(transactions[0]['account_name'].split())

    identifier = ObjectId().binary[4:].hex()
    # returns the hexadecimal string of the last 8 bytes of object id, which are the random value and the counter. This is because
    # the id I am constructing for journals will already include the date, and this is to ensure that two journal ids cannot be identical

    entry['journal_id'] = date + transaction1 + transaction2 + identifier
    # each journal ID will be the date, followed by the names of the first 2 accounts affected, followed by a random identifier.

    message = DBA.insert('Journal', entry, user_id)
    return message

@app.put('/journal/approve')
async def approve_journal_entry(journal_id : str, user_id : str):
    entry = DBA.get_one('Journal', {'journal_id': journal_id})

    entry['approved_status'] = 'approved'
    assign_journal_pages(entry)

    # transactions = entry['transactions']
    # for trans in transactions:
    #
    #     DBA.update_account_balance(trans['post_reference'], trans['side'], trans['balance'], )
    DBA.update('Journal',{'journal_id':journal_id}, entry, user_id)

@app.put('/journal/reject')
async def reject_journal_entry(journal_id: str, comment: str, user_id: str):
    entry = DBA.get_one('Journal', {'journal_id': journal_id})

    entry['approved_status'] = 'rejected'
    entry['comment']= comment
    # assign_journal_pages(entry)
    DBA.update('Journal', {'journal_id': journal_id}, entry, user_id)

def assign_journal_pages(entry: JournalEntry):
    transactions = entry['transactions']
    journals = fetch_journal(status=ApprovedStatus.approved)

    total_trans_count = 0

    if journals is not None:
        for jentry in journals:
            total_trans_count += len(jentry['transactions'])  # gets the total number of transaction lines in the approved journal

    for trans in transactions:
        total_trans_count += 1
        journal_page = ((total_trans_count - 1) // JOURNAL_PAGE_LENGTH) + 1
        trans['journal_page'] = f"J{journal_page}"


def sum_transaction_list(transactions: List[Transaction]):
    balance = 0
    if transactions is not None:
        for trans in transactions:
            trans_bal = trans['balance']

            if trans_bal is str:
                trans['balance'] = int(trans_bal)
                trans_bal = int(trans_bal)

            if trans['side'] == "debit":
                #print(f"Adding {trans['balance']}")
                balance += trans_bal
            elif trans['side'] == "credit":
                #print(f"Subtracting {trans['balance']}")
                balance -= trans_bal

    return balance


@app.get("/ledger/transactions")
async def get_ledger_transactions(account_id: int=0):
    """
        Returns a list all approved transactions for a specified account, skipping the journal entry data entirely.
        It will return only the approved transactions, and pending and rejected transactions should not be displayed independently of their journal entry data.
        If no account_id is specified, it will return all approved journal entries, making this case excellent for the journal page.

        :param account_id:
        :return list of transaction objects:
        """
    return fetch_ledger_transactions(account_id)

def fetch_ledger_transactions(account_id: int = 0):

    entries = fetch_journal(status=ApprovedStatus.approved)

    if entries is None:
        return {}  # there are no entries yet, so it returns empty but valid data, so it does not cause an error

    trans_list = []

    if account_id == 0: # gets all transactions from ledger
        for entry in entries:
            entry_transactions = entry['transactions']
            for trans in entry_transactions:
                trans_list.append(trans)

    else:
        for entry in entries:
            entry_transactions = entry['transactions']
            for trans in entry_transactions:
                if trans['post_reference'] == account_id:
                    trans_list.append(trans)

    return trans_list

@app.post("/upload_file")
async def upload_file(user_id: str, file: UploadFile = File(...) ):
    file_bytes = await file.read()
    encoded = base64.b64encode(file_bytes).decode('utf-8')
    file_upload = {
        "file_id": str(ObjectId()),
        "file_name": file.filename,
        "content_type": file.content_type,
        "file_data": encoded
    }
    DBA.insert('Uploads', file_upload, user_id)

@app.get("/download_file")
async def download_file(file_id: str):
    file_download = DBA.get_one('Uploads', {"file_id": file_id})
    decoded = base64.b64decode(file_download['file_data'])
    return Response(content=decoded, media_type=file_download['content_type'],
                    headers={"Content-Disposition": f"attachment; filename={file_download['file_name']}"})