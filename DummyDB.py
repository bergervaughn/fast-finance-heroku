from datetime import date, timedelta, datetime
from fastapi import HTTPException
from typing import List

import FFEmail
from userinfo import User, Role, NewUserRequest

user_table: List[User] = [
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

new_user_table: List[NewUserRequest] = [

]

def get_user(check_id: str):
    for u in user_table:
        if check_id == u.id:
            return u
    raise HTTPException(404, detail={"Error": f"Used ID {check_id} not found"})

def check_outdated_passwords():
    current = date.today()
    outdated = current + timedelta(days=3)
    for u in user_table:
        pass_ex_dt = datetime.strptime(u.password_expiration, "%Y-%m-%d").date() #converts the password expiration string to a datetime object for comparison
        if pass_ex_dt < current:
            u.status = False
            #print(f"{u.id} has an expired password and has been suspended!")
            FFEmail.send_email([u.email], "Account Suspended", f"Hello, {u.first_name}. Your password has expired and your account has become suspended.")
        elif pass_ex_dt < outdated:
            #print(f"{u.id} has a password about to expire!")
            FFEmail.send_email([u.email],"Password about to expire", f"Hello, {u.first_name}. Your password is set to expire soon. Please update it so your account does not become suspended.")



check_outdated_passwords()