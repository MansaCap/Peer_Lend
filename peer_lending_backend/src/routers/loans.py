# FastAPI router for handling loan-related endpoints #

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.loan_service import LoanService
from schemas.loan_lifecycle import LoanApply, LoanApprove, LoanDisburse, LoanRepay

router = APIRouter()
service = LoanService()

@router.post("/apply")
def apply(payload: LoanApply, db: Session = Depends(get_db)):
    return service.apply(db, payload)

@router.post("/approve")
def approve(payload: LoanApprove, db: Session = Depends(get_db)):
    return service.approve(db, payload)

@router.post("/disburse")
def disburse(payload: LoanDisburse, db: Session = Depends(get_db)):
    return service.disburse(db, payload)

@router.post("/repay")
def repay(payload: LoanRepay, db: Session = Depends(get_db)):
    return service.repay(db, payload)
