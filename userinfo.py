from pydantic import BaseModel
from enum import Enum

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
    email: str = "bergervaughn@gmail.com" # default is my email
    role: Role
    status: bool = True
    first_name: str
    last_name: str

