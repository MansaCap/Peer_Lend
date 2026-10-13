from fastapi import APIRouter, status

from peer_lending_backend.src.schemas.identity import (
    IdentityKYCRequest,
    IdentityVerifyRequest,
)

router = APIRouter()


@router.post("/verify", status_code=status.HTTP_202_ACCEPTED)
def verify_identity(payload: IdentityVerifyRequest):
    return {
        "borrower_id": payload.borrower_id,
        "status": "pending",
        "message": "Identity verification request received",
    }


@router.post("/kyc", status_code=status.HTTP_202_ACCEPTED)
def submit_kyc(payload: IdentityKYCRequest):
    return {
        "borrower_id": payload.borrower_id,
        "status": "pending",
        "message": "KYC submission received",
    }
