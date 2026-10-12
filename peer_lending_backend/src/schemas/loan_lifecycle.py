# Pydantic models for the Loan Management entity #
# These models define the structure of loan management-related data for API requests and responses.

from pydantic import BaseModel
from decimal import Decimal

class LoanApply(BaseModel):
    borrower_id: int
    amount: Decimal
    interest_rate: Decimal
    term_months: int

class LoanApprove(BaseModel):
    loan_id: int

class LoanDisburse(BaseModel):
    loan_id: int

class LoanRepay(BaseModel):
    loan_id: int
    amount: Decimal

class LoanDefault(BaseModel):
    loan_id: int

class LoanLiquidate(BaseModel):
    loan_id: int

