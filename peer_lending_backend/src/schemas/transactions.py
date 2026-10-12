# Pydantic models for the Transaction entity #
# These models define the structure of transaction-related data for API requests and responses.


from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class TransactionBase(BaseModel):
    loan_id: int
    type: str
    amount: Decimal

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: int
    created_at: datetime

    class Config:
        orm_mode = True
