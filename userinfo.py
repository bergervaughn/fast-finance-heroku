from datetime import date

from pydantic import BaseModel
from enum import Enum
from typing import List

class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    accountant = "accountant"

class Status(str, Enum):
    active = "active"
    suspended = "suspended"

class User(BaseModel):
    id: str
    hashed_pass: str
    past_passwords: List[str] = []
    email: str = "bergervaughn@gmail.com" # default is my email
    role: Role
    status: bool = True
    first_name: str
    last_name: str
    dob: str = "01-01-1900"
    failed_attempts: int = 0
    password_expiration: str = "01-05-2025"
    security_question: str = "What is your mother's maiden name?"
    security_answer: str = "Jones"

class NewUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    dob: str

class Email(BaseModel):
    recipient: str
    subject: str
    body: str


# class PastPasswords(BaseModel):
#     pass_id: str
#     user_id: str
#     hashed_pass: str
#     date_created: date