import main
import json
from userinfo import User
import asyncio

async def main_method():
    # email = '{"recipient": "bergervaughn@gmail.com","subject": "API driver test","body": "This is a test of the API using my pycharm driver file"}'

    # task = asyncio.create_task(main.send_email(json.loads(email)))
    #task = main.fetch_users()
    #task = main.forgot_pass("VBerger2025")
    #task = main.login("user1234","hashed_password_example")

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
    # task = main.register_user(user, "VBerger2025")

    task = main.update_user_field("WAfton1996", {"first_name":"William"}, "VBerger2025")
    # user_req = {
    #     "first_name": "Barack",
    #     "last_name": "Obama",
    #     "email": "president@whitehouse.gov",
    #     "dob" : "1961-08-04"
    # }
    # #task = main.new_user(user_req)
    # task = main.delete_new_user_request("president@whitehouse.gov")

    print(await task)

asyncio.run(main_method())
