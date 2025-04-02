from pydantic import BaseModel
from enum import Enum
from typing import List

JOURNAL_PAGE_LENGTH = 20

class NormalSide(str, Enum):
    debit = "debit"
    credit = "credit"

class Statement(str, Enum):
    BS = "BS"  # balance sheet
    IS = "IS"  # income statement
    RE = "RE"  # retained earnings

class ApprovedStatus(str, Enum):
    approved = "approved"
    pending = "pending"
    rejected = "rejected"

class Account(BaseModel):
    account_id: int
    account_name : str
    order: int
    description : str = ""
    normal_side : NormalSide
    category : str
    sub_category : str
    initial_balance : int = 0
    debit : int = 0
    credit : int = 0
    statement : Statement
    comment: str = ""
    status: bool = True

class Transaction(BaseModel):
    date: str # "DD/MM"
    account_name : str
    balance : int
    side : NormalSide
    description: str = ""
    post_reference: str # references an account ID
    journal_page : str = "" # calculated automatically on the backend

class JournalEntry(BaseModel):
    journal_id : str
    date : str = ""
    transactions : List = []
    approved_status : ApprovedStatus = "pending"
    comment : str = ""

