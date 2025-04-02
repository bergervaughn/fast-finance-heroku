import DatabaseAccess
import main
import json

from FinanceDataModels import JournalEntry
from main import *
from userinfo import User
import asyncio

# async def main_method():
    # email = '{"recipient": "bergervaughn@gmail.com","subject": "API driver test","body": "This is a test of the API using my pycharm driver file"}'

    # task = asyncio.create_task(main.send_email(json.loads(email)))
    #task = main.fetch_users()
    #task = main.forgot_pass("VBerger2025")
    #task = main.login("VBerger2025","1Mn!")

    # user = {
    #     "user_id": "WAfton1996",
    #     "hashed_pass": "password",
    #     "past_passwords": [],
    #     "email": "bergervaughn@gmail.com",
    #     "role": "manager",
    #     "status": True,
    #     "first_name": "Billiam",
    #     "last_name": "Afton",
    #     "profile_picture": 4,
    #     "dob": "1944-05-17",
    #     "failed_attempts": 0,
    #     "password_expiration": "2025-04-05",
    #     "security_answers": ["1", "2", "3"],
    #     "suspension_start": "",
    #     "suspension_end": ""
    # }
    # user = {
    #     "user_id": "JDoe1234",
    #     "hashed_pass": "password",
    #     "past_passwords": [],
    #     "email": "bergervaughn@gmail.com",
    #     "role": "accountant",
    #     "status": True,
    #     "first_name": "John",
    #     "last_name": "Doe",
    #     "profile_picture": 4,
    #     "dob": "1980-05-17",
    #     "failed_attempts": 0,
    #     "password_expiration": "2025-04-05",
    #     "security_answers": ["1","2","3"],
    #     "suspension_start": "",
    #     "suspension_end": ""
    # }
    # task = main.register_user(user, "VBerger2025")

    #DatabaseAccess.remove_id_recursive()
    #DatabaseAccess.remove_referenced_object_ids()
    #DatabaseAccess.check_outdated_passwords()
    #task = main.get_expired_passwords()

    #task = main.update_user_attribute("WAfton1996", {"first_name":"William"}, "VBerger2025")
    # user_req = {
    #     "email": "president@whitehouse.gov",
    #     "first_name": "Barack",
    #     "last_name": "Obama",
    #     "dob" : "1961-08-04",
    #     "hashed_pass" : "obamna",
    #     "role" : "manager",
    #     "security_answers" : ["1", "2", "3"]
    # }
    # task = main.new_user(user_req)
    #task = main.delete_new_user_request("president@whitehouse.gov", "VBerger2025")
    #task = main.get_accounts()
    #print( DatabaseAccess.get('Events'))
    # account = {
    #     "account_id": 10000001,
    #     "account_name": "Accounts Receivable",
    #     "description": "",
    #     "normal_side": "debit",
    #     "category": "Assets",
    #     "sub_category": "Current Assets",
    #     "initial_balance": 0,
    #     "debit": 0,
    #     "credit": 0,
    #     "balance": 0,
    #     "statement": "BS",
    #     "comment": "",
    #     "status": True
    # }
    #
    # task = main.create_account(account, "VBerger2025")

    # entry = \
    # {
    #     "transactions": [
    #     {
    #         "date": "2025-04-04",
    #         "account_name": "Accounts Receivable",
    #         "balance": 500,
    #         "side": "credit",
    #         "post_reference": 10000001
    #     },
    #     {
    #         "date" : "2025-04-04",
    #         "account_name": "Cash",
    #         "balance": 500,
    #         "side": "debit",
    #         "post_reference" : 10000000
    #     }],
    #     "approved_status" : "approved"
    # }

    # entry = {
    #     "transactions": [
    #         {
    #             "date": "2025-04-04",
    #             "account_name": "Cash",
    #             "balance": 500,
    #             "side": "debit",
    #             "post_reference": 10000001
    #         }],
    #     "approved_status": "approved"
    # }

    # task = main.post_journal_entry(entry, user_id="VBerger2025")


    #
    # task = main.get_ledger_transactions()
    # print (await task)

async def insert_user(user):
    await register_user(user, "VBerger2025")
    print(f"Inserted user {user['user_id']}")

async def insert_account(account):
    await create_account(account, "VBerger2025")
    print(f"Inserted account: {account['account_id']}")

async def insert_journal_entry(entry):
    await post_journal_entry(entry, "VBerger2025")
    print(f"Inserted journal entry: {entry['journal_id']}")

async def insert_user_request(user_req):
    await new_user(user_req)
    print(f"Inserted new user request: {user_req['email']}")

async def insert_data(data):

    if "user_id" in data:
        await insert_user(data)
    elif "account_id" in data:
        await insert_account(data)
    elif "journal_id" in data:
        await insert_journal_entry(data)
    elif "email_id" in data and "user_id" not in data:
        await insert_user_request(data)

async def insert_multiple_data(data_list):
    tasks = [insert_data(data) for data in data_list]
    await asyncio.gather(*tasks)

#if __name__ == "__main__":
big_data_list = \
[
    {
        "user_id": "VBerger0125",
        "hashed_pass": "password",
        "past_passwords": [],
        "email": "bergervaughn@gmail.com",
        "role": "admin",
        "status": True,
        "first_name": "Vaughn",
        "last_name": "Berger",
        "profile_picture": 0,
        "dob": "2000-08-16",
        "failed_attempts": 0,
        "password_expiration": "",
        "security_answers": ["1", "2", "3"],
        "suspension_start": "",
        "suspension_end": ""
    },
    {
        "user_id": "monter0225",
        "hashed_pass": "password",
        "past_passwords": [],
        "email": "montgomeryrussel2000@gmail.com",
        "role": "manager",
        "status": True,
        "first_name": "Monte",
        "last_name": "Russel",
        "profile_picture": 0,
        "dob": "2001-09-14",
        "failed_attempts": 0,
        "password_expiration": "",
        "security_answers": ["1", "2", "3"],
        "suspension_start": "",
        "suspension_end": ""
    },
    {
        "user_id": "tcaffrey0325",
        "hashed_pass": "password",
        "past_passwords": [],
        "email": "trevorcaffrey@gmail.com",
        "role": "accountant",
        "status": True,
        "first_name": "Trevor",
        "last_name": "Caffrey",
        "profile_picture": 0,
        "dob": "2002-01-01",
        "failed_attempts": 0,
        "password_expiration": "",
        "security_answers": ["1", "2", "3"],
        "suspension_start": "",
        "suspension_end": ""
    },
    {
        "email": "honestabe@gmail.com",
        "first_name": "Abraham",
        "last_name": "Lincoln",
        "dob" : "1809-02-12",
        "hashed_pass" : "password",
        "role" : "accountant",
        "security_answers" : ["1", "2", "3"]
    },
    {
        "account_id": 1000,
        "account_name": "Cash",
        "description": "",
        "normal_side": "debit",
        "category": "Assets",
        "sub_category": "Current Assets",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    {
        "journal_id" : "",
        "date": "",
        "transactions": [
            {
                "date": "",
                "account_name": "",
                "balance": 0,
                "side": "",
                "post_reference": 0
            },
            {
                "date": "",
                "account_name": "",
                "balance": 0,
                "side": "",
                "post_reference": 0
            }],
        "approved_status": ""
    }
]

asyncio.run(insert_data(big_data_list))
