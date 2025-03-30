from pydantic import BaseModel
from enum import Enum
from typing import List

class NormalSide(str, Enum):
    debit = "debit"
    credit = "credit"

class Statement(str, Enum):
    BS = "BS"
    IS = "IS"
    RE = "RE"

class FinancialAccount(BaseModel):
    account_id: int
    account_name : str
    description : str = ""
    normal_side : NormalSide
    category : str
    sub_category : str
    initial_balance : int = 0
    debit : int = 0
    credit : int = 0
    balance : int = 0
    statement : Statement
    comment: str = ""
