from pydantic import BaseModel
from enum import Enum
from typing import List

class NormalSide(str, Enum):
    debit = "debit"
    credit = "credit"

class Statement(str, Enum):
    BS = "BS"  # balance sheet
    IS = "IS"  # income statement
    RE = "RE"  # retained earnings

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

class LedgerEntry(BaseModel):
    date : str = "DD/MM"
    lines : List = []

class LedgerLine(BaseModel):
    name : str
    side : NormalSide
    amount : int
