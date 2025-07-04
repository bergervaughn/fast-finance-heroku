import DatabaseAccess
import main
import json

from DatabaseAccess import delete_entire_database
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

async def approve_all_journals():
    tasks = [main.approve_journal_entry(journal['journal_id'], "VBerger2025") for journal in DBA.get('Journal')]
    await asyncio.gather(*tasks)


#if __name__ == "__main__":
big_data_list = \
[
    # Users
    {
        "user_id": "VBerger2025",
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
        "password_expiration": "2025-6-01",
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
        "password_expiration": "2025-04-05",
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
        "password_expiration": "2025-01-01",
        "security_answers": ["1", "2", "3"],
        "suspension_start": "",
        "suspension_end": ""
    },
    # user requests
    {
        "email": "honestabe@gmail.com",
        "first_name": "Abraham",
        "last_name": "Lincoln",
        "dob" : "1809-02-12",
        "hashed_pass" : "password",
        "role" : "accountant",
        "security_answers" : ["1", "2", "3"]
    },
    # accounts
    ## assets
    {
        "account_id": 10000100,
        "account_name": "Cash",
        "order": 101,
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
        "account_id": 10000101,
        "account_name": "Accounts Receivable",
        "order": 102,
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
        "account_id": 10000102,
        "account_name": "Prepaid Rent",
        "order": 103,
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
        "account_id": 10000103,
        "account_name": "Prepaid Insurance",
        "order": 104,
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
        "account_id": 10000104,
        "account_name": "Supplies",
        "order": 105,
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
    # Property Plant & Equipment
    {
        "account_id": 10000200,
        "account_name": "Office Equipment",
	    "order": 106,
        "description": "",
        "normal_side": "debit",
        "category": "Assets",
        "sub_category": "Property Plant & Equipment",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000201,
        "account_name": "Accumulated Depreciation",
	    "order": 106,
        "description": "",
        "normal_side": "credit",
        "category": "Assets",
        "sub_category": "Contra-Assets",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    ## liabilities
    {
        "account_id": 10000300,
        "account_name": "Accounts Payable",
        "order": 107,
        "description": "",
        "normal_side": "credit",
        "category": "Liabilities",
        "sub_category": "Current Liabilities",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000301,
        "account_name": "Salaries Payable",
        "order": 108,
        "description": "",
        "normal_side": "credit",
        "category": "Liabilities",
        "sub_category": "Current Liabilities",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000302,
        "account_name": "Unearned Revenue",
        "order": 109,
        "description": "",
        "normal_side": "credit",
        "category": "Liabilities",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    ## Equity
    {
        "account_id": 10000303,
        "account_name": "Contributed Capital",
        "order": 110,
        "description": "",
        "normal_side": "credit",
        "category": "Stakeholder's Equity",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000304,
        "account_name": "Retained Earnings",
        "order": 111,
        "description": "",
        "normal_side": "credit",
        "category": "Stakeholder's Equity",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "BS",
        "comment": "",
        "status": True
    },
    ## Revenues
    {
        "account_id": 10000500,
        "account_name": "Service Revenue",
        "order": 112,
        "description": "",
        "normal_side": "credit",
        "category": "Revenues",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    ## Expenses
    {
        "account_id": 10000600,
        "account_name": "Insurance Expense",
        "order": 113,
        "description": "",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000601,
        "account_name": "Depreciation Expense",
        "order": 114,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000602,
        "account_name": "Rent Expense",
        "order": 115,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000603,
        "account_name": "Supplies Expense",
        "order": 116,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000604,
        "account_name": "Salaries Expense",
        "order": 117,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000605,
        "account_name": "Telephone Expense",
        "order": 118,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000606,
        "account_name": "Utilities Expense",
        "order": 119,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    {
        "account_id": 10000607,
        "account_name": "Advertising Expense",
        "order": 120,
        "description": "N/A",
        "normal_side": "debit",
        "category": "Expenses",
        "sub_category": "N/A",
        "initial_balance": 0,
        "debit": 0,
        "credit": 0,
        "balance": 0,
        "statement": "IS",
        "comment": "",
        "status": True
    },
    #journal entries
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-04",
                "account_name": "Cash",
                "balance": 10000,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-04",
                "account_name": "Accounts Receivable",
                "balance": 1500,
                "side": "debit",
                "post_reference": 10000101
            },
            {
                "date": "2025-04-04",
                "account_name": "Supplies",
                "balance": 1250,
                "side": "debit",
                "post_reference": 10000104
            },
            {
                "date": "2025-04-04",
                "account_name": "Office Equipment",
                "balance": 7500,
                "side": "debit",
                "post_reference": 10000200
            },
            {
                "date": "2025-04-04",
                "account_name": "Contributed Capital",
                "balance": 20250,
                "side": "credit",
                "post_reference": 10000303
            }],
        "approved_status": ""
    },
    {
        "journal_id" : "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-04",
                "account_name": "Prepaid Rent",
                "balance": 4500,
                "side": "debit",
                "post_reference": 10000102
            },
            {
                "date": "2025-04-04",
                "account_name": "Cash",
                "balance": 4500,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id" : "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-04",
                "account_name": "Prepaid Insurance",
                "balance": 1800,
                "side": "debit",
                "post_reference": 10000103
            },
            {
                "date": "2025-04-04",
                "account_name": "Cash",
                "balance": 1800,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-06",
                "account_name": "Cash",
                "balance": 3000,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-06",
                "account_name": "Unearned Revenue",
                "balance": 3000,
                "side": "credit",
                "post_reference": 10000302
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-07",
                "account_name": "Office Equipment",
                "balance": 1800,
                "side": "debit",
                "post_reference": 10000200
            },
            {
                "date": "2025-04-07",
                "account_name": "Accounts Payable",
                "balance": 1800,
                "side": "credit",
                "post_reference": 10000300
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-08",
                "account_name": "Cash",
                "balance": 800,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-08",
                "account_name": "Accounts Receivable",
                "balance": 800,
                "side": "credit",
                "post_reference": 10000101
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-11",
                "account_name": "Advertising Expense",
                "balance": 120,
                "side": "debit",
                "post_reference": 10000607
            },
            {
                "date": "2025-04-11",
                "account_name": "Cash",
                "balance": 120,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-12",
                "account_name": "Accounts Payable",
                "balance": 800,
                "side": "debit",
                "post_reference": 10000300
            },
            {
                "date": "2025-04-12",
                "account_name": "Cash",
                "balance": 800,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-15",
                "account_name": "Accounts Receivable",
                "balance": 2250,
                "side": "debit",
                "post_reference": 10000101
            },
            {
                "date": "2025-04-15",
                "account_name": "Service Revenue",
                "balance": 2250,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-15",
                "account_name": "Salaries Expense",
                "balance": 400,
                "side": "debit",
                "post_reference": 10000604
            },
            {
                "date": "2025-04-15",
                "account_name": "Cash",
                "balance": 400,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-15",
                "account_name": "Cash",
                "balance": 3175,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-15",
                "account_name": "Service Revenue",
                "balance": 3175,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-18",
                "account_name": "Supplies",
                "balance": 750,
                "side": "debit",
                "post_reference": 10000104
            },
            {
                "date": "2025-04-18",
                "account_name": "Cash",
                "balance": 750,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-22",
                "account_name": "Accounts Receivable",
                "balance": 1100,
                "side": "debit",
                "post_reference": 10000101
            },
            {
                "date": "2025-04-22",
                "account_name": "Service Revenue",
                "balance": 1100,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-22",
                "account_name": "Cash",
                "balance": 1850,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-22",
                "account_name": "Service Revenue",
                "balance": 1850,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-22",
                "account_name": "Cash",
                "balance": 1600,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-22",
                "account_name": "Accounts Receivable",
                "balance": 1600,
                "side": "credit",
                "post_reference": 10000101
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-27",
                "account_name": "Salaries Expense",
                "balance": 400,
                "side": "debit",
                "post_reference": 10000604
            },
            {
                "date": "2025-04-27",
                "account_name": "Cash",
                "balance": 400,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-28",
                "account_name": "Telephone Expense",
                "balance": 130,
                "side": "debit",
                "post_reference": 10000605
            },
            {
                "date": "2025-04-28",
                "account_name": "Cash",
                "balance": 130,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-29",
                "account_name": "Utilities Expense",
                "balance": 200,
                "side": "debit",
                "post_reference": 10000606
            },
            {
                "date": "2025-04-29",
                "account_name": "Cash",
                "balance": 200,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-29",
                "account_name": "Cash",
                "balance": 2050,
                "side": "debit",
                "post_reference": 10000100
            },
            {
                "date": "2025-04-29",
                "account_name": "Service Revenue",
                "balance": 2050,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-29",
                "account_name": "Accounts Receivable",
                "balance": 1000,
                "side": "debit",
                "post_reference": 10000101
            },
            {
                "date": "2025-04-29",
                "account_name": "Service Revenue",
                "balance": 1000,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "normal",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-29",
                "account_name": "Salaries Expense",
                "balance": 4500,
                "side": "debit",
                "post_reference": 10000604
            },
            {
                "date": "2025-04-29",
                "account_name": "Cash",
                "balance": 4500,
                "side": "credit",
                "post_reference": 10000100
            }],
        "approved_status": ""
    },
    #adjusting journal entries
    {
        "journal_id": "",
        "date": "",
        "journal_type" : "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Insurance Expense",
                "balance": 150,
                "side": "debit",
                "post_reference": 10000600
            },
            {
                "date": "2025-04-30",
                "account_name": "Prepaid Insurance",
                "balance": 150,
                "side": "credit",
                "post_reference": 10000103
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type" : "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Supplies Expense",
                "balance": 980,
                "side": "debit",
                "post_reference": 10000603
            },
            {
                "date": "2025-04-30",
                "account_name": "Supplies",
                "balance": 980,
                "side": "credit",
                "post_reference": 10000104
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Depreciation Expense",
                "balance": 500,
                "side": "debit",
                "post_reference": 10000601
            },
            {
                "date": "2025-04-30",
                "account_name": "Accumulated Depreciation",
                "balance": 500,
                "side": "credit",
                "post_reference": 10000201
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Salaries Expense",
                "balance": 20,
                "side": "debit",
                "post_reference": 10000604
            },
            {
                "date": "2025-04-30",
                "account_name": "Salaries Payable",
                "balance": 20,
                "side": "credit",
                "post_reference": 10000301
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Rent Expense",
                "balance": 1500,
                "side": "debit",
                "post_reference": 10000602
            },
            {
                "date": "2025-04-30",
                "account_name": "Prepaid Rent",
                "balance": 1500,
                "side": "credit",
                "post_reference": 10000102
            }],
        "approved_status": ""
    },
    {
        "journal_id": "",
        "date": "",
        "journal_type": "adjusting",
        "description": "",
        "transactions": [
            {
                "date": "2025-04-30",
                "account_name": "Unearned Revenue",
                "balance": 2000,
                "side": "debit",
                "post_reference": 10000302
            },
            {
                "date": "2025-04-30",
                "account_name": "Service Revenue",
                "balance": 2000,
                "side": "credit",
                "post_reference": 10000500
            }],
        "approved_status": ""
    },
]

delete_entire_database()
asyncio.run(insert_multiple_data(big_data_list))
asyncio.run(approve_all_journals())

#asyncio.run(main.get_ratios())
# async def main_function():
#     task = main.get_accounts()
#     print(await task)
# asyncio.run(main_function())