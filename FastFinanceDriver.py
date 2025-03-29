import main
import json
import asyncio

async def main_method():
    # email = '{"recipient": "bergervaughn@gmail.com","subject": "API driver test","body": "This is a test of the API using my pycharm driver file"}'

    # task = asyncio.create_task(main.send_email(json.loads(email)))
    #task = main.fetch_users()

    task = main.login("user1234","hashed_password_example")

    print(await task)

asyncio.run(main_method())
