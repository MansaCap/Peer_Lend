# Pydantic models for the Loan entity #
# These models define the structure of loan-related data for API requests and responses.

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LoanBase(BaseModel):
    borrower_id: int
    amount: Decimal
    interest_rate: Decimal
    term_months: int

class LoanCreate(LoanBase):
    pass

class LoanUpdateStatus(BaseModel):
    loan_id: int
    status: str

class LoanResponse(LoanBase):
    loan_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
