# Pydantic models for the Repayment entity #
# These models define the structure of repayment-related data for API requests and responses.


from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class RepaymentBase(BaseModel):
    loan_id: int
    amount: Decimal

class RepaymentCreate(RepaymentBase):
    pass

class RepaymentResponse(RepaymentBase):
    repayment_id: int
    paid_at: datetime

    class Config:
        orm_mode = True
