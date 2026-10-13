# Service class for managing Loan operations using the LoanRepository #

from sqlalchemy.orm import Session

from peer_lending_backend.src.repositories.loan_repository import LoanRepository
from peer_lending_backend.src.schemas.loan_lifecycle import (
    LoanApply,
    LoanApprove,
    LoanDisburse,
    LoanRepay,
)

class LoanService:

    def __init__(self):
        self.repo = LoanRepository()

    def apply(self, db: Session, payload: LoanApply):
        return self.repo.create(db, payload)

    def approve(self, db: Session, payload: LoanApprove):
        return self.repo.update_status(db, payload.loan_id, "approved")

    def disburse(self, db: Session, payload: LoanDisburse):
        return self.repo.update_status(db, payload.loan_id, "disbursed")

    def repay(self, db: Session, payload: LoanRepay):
        # repayment logic will be added in Step C
        return {"message": "Repayment placeholder"}
