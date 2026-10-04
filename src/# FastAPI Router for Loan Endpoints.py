# FastAPI Router for Loan Endpoints

from fastapi import APIRouter, Depends
from .schemas import LoanDisburseRequest, LoanRepayRequest
from .service import disburse_loan, process_repayment

router = APIRouter(prefix="/loan", tags=["Loan"])

@router.post("/disburse")
async def disburse_loan_funds(payload: LoanDisburseRequest):
    return await disburse_loan(payload)

@router.post("/repay")
async def repay_loan(payload: LoanRepayRequest):
    return await process_repayment(payload)
