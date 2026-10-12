# Pydantic models for the Payback Analysis Tally entity #
# These models define the structure of payback analysis tally-related data for API requests and responses.


from pydantic import BaseModel
from decimal import Decimal

class PaybackAnalysisTallyBase(BaseModel):
    total_loans: int
    avg_pd: Decimal
    avg_ltv: Decimal
    avg_repayment_time: int

class PaybackAnalysisTallyResponse(PaybackAnalysisTallyBase):
    tally_id: int

    class Config:
        orm_mode = True
