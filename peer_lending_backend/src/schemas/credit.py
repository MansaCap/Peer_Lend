# Pydantic models for the Credit Score entity #
# These models define the structure of credit score-related data for API requests and responses.

from pydantic import BaseModel, Field

class CreditScoreRequest(BaseModel):
    borrower_id: int
    income: float = Field(gt=0)
    existing_debt: float = Field(ge=0)
    payment_history_score: float = Field(ge=0, le=100)

class CreditScoreResponse(BaseModel):
    borrower_id: int
    score: float
