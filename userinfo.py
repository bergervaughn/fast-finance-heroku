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
    past_passwords: List[PastPasswords]
    email: str = "bergervaughn@gmail.com" # default is my email
    role: Role
    status: bool = True
    first_name: str
    last_name: str
    failed_attempts: int = 0

class NewUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    dob: str

class PastPasswords(BaseModel):
