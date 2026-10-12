# Pydantic models for the Borrower Payback Status entity #
# These models define the structure of borrower payback status-related data for API requests and responses.


from pydantic import BaseModel
from decimal import Decimal

class BorrowerPaybackStatusBase(BaseModel):
    borrower_id: int
    total_loans: int
    total_repaid: Decimal
    delinquency_rate: Decimal
    risk_grade: str

class BorrowerPaybackStatusResponse(BorrowerPaybackStatusBase):
    status_id: int

    class Config:
        orm_mode = True
