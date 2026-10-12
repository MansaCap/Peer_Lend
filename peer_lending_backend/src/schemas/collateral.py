# Pydantic models for the Collateral entity #
# These models define the structure of collateral-related data for API requests and responses.

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class CollateralBase(BaseModel):
    borrower_id: int
    type: str
    value: Decimal

class CollateralCreate(CollateralBase):
    verification_status: str = "pending"

class CollateralResponse(CollateralBase):
    collateral_id: int
    verification_status: str
    created_at: datetime

    class Config:
        orm_mode = True
