import DatabaseAccess
import main
import json
from userinfo import User
import asyncio

async def main_method():
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
    task = main.get_expired_passwords()

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

    print(await task)

asyncio.run(main_method())
