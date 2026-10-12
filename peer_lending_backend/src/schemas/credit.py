# Pydantic models for the Credit Score entity #
# These models define the structure of credit score-related data for API requests and responses.

from pydantic import BaseModel

class CreditScoreRequest(BaseModel):
    borrower_id: int

class CreditScoreResponse(BaseModel):
    borrower_id: int
    score: float
