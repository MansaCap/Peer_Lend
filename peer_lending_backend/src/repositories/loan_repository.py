# Repository class for managing Loan entities in the database using SQLAlchemy #

from sqlalchemy.orm import Session
from models.loans import Loan
from schemas.loan import LoanCreate

class LoanRepository:
    def create(self, db: Session, payload: LoanCreate):
        loan = Loan(
            borrower_id=payload.borrower_id,
            amount=payload.amount,
            interest_rate=payload.interest_rate,
            term_months=payload.term_months,
            status="pending",
        )
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    def get(self, db: Session, loan_id: int):
        return db.query(Loan).filter(Loan.loan_id == loan_id).first()

    def update_status(self, db: Session, loan_id: int, status: str):
        loan = self.get(db, loan_id)
        if not loan:
            return None
        loan.status = status
        db.commit()
        db.refresh(loan)
        return loan

    def list_by_borrower(self, db: Session, borrower_id: int):
        return db.query(Loan).filter(Loan.borrower_id == borrower_id).all()
