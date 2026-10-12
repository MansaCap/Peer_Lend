# Repository class for managing Repayment entities in the database using SQLAlchemy #

from sqlalchemy.orm import Session
from models.repayments import Repayment
from schemas.repayment import RepaymentCreate

class RepaymentRepository:
    def create(self, db: Session, payload: RepaymentCreate):
        repayment = Repayment(
            loan_id=payload.loan_id,
            amount=payload.amount,
        )
        db.add(repayment)
        db.commit()
        db.refresh(repayment)
        return repayment

    def list_by_loan(self, db: Session, loan_id: int):
        return db.query(Repayment).filter(Repayment.loan_id == loan_id).all()
