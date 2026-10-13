# Pydantic models for the Identity Verification and KYC entities #
# These models define the structure of identity verification and KYC-related data for API requests and responses.


from datetime import date

from pydantic import BaseModel, HttpUrl


class IdentityVerifyRequest(BaseModel):
    borrower_id: int
    full_name: str
    date_of_birth: date
    id_type: str
    id_number: str


class IdentityKYCRequest(BaseModel):
    borrower_id: int
    full_name: str
    address: str
    country: str
    document_url: HttpUrl
