from datetime import datetime
from typing import List
from userinfo import User, Role, NewUserRequest

db: List[User] = [
    User(
        id="testAdmin",
        hashed_pass="temp",
        # email is default for now so this test user can receive emails
        role = Role.admin,
        status=True,
        first_name="Dave",
        last_name="Administrator"
    ),
    User(
        id="sampleAccountant",
        hashed_pass="temp",
        role=Role.accountant,
        status=True,
        first_name="John",
        last_name="Accounting"
    )
]

def get_user(check_id: str):
    for u in db:
        if check_id == u.id:
            return u
    raise NameError(f"User ID: {check_id} not found.")

# def check_outdated_passwords():
#     current_time = datetime
#     for u in db:
#         if