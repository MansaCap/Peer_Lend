# Pydantic models for the Identity Verification and KYC entities #
# These models define the structure of identity verification and KYC-related data for API requests and responses.


from pydantic import BaseModel

class IdentityVerify(BaseModel):
    user_id: int
    document_type: str
    document_number: str

class IdentityKYC(BaseModel):
    user_id: int
    country: str
    id_number: str
