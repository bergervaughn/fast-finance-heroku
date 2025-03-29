from datetime import date

from pydantic import BaseModel
from enum import Enum
from typing import List

class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    accountant = "accountant"

#
# class Status(str, Enum):
#     active = "active"
#     suspended = "suspended"

class User(BaseModel):
    user_id: str
    hashed_pass: str
    past_passwords: List[str] = []
    email: str = "bergervaughn@gmail.com" # default is my email
    role: Role
    status: bool = True
    first_name: str
    last_name: str
    profile_picture : int = 0
    dob: str = "1900-01-01"
    failed_attempts: int = 0
    password_expiration: str = "2025-01-05"
    security_answers: List[str] = []
    suspension_start : str = ""
    suspension_end : str = ""

class NewUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    dob: str
    hashed_pass: str
    role : Role

class Email(BaseModel):
    recipient: str
    subject: str
    body: str


# class PastPasswords(BaseModel):
#     pass_id: str
#     user_id: str
#     hashed_pass: str
#     date_created: date