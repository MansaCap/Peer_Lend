# Repository class for managing Transaction entities in the database using SQLAlchemy #


from sqlalchemy.orm import Session
from models.transactions import Transaction
from schemas.transaction import TransactionCreate

class TransactionRepository:
    def create(self, db: Session, payload: TransactionCreate):
        tx = Transaction(
            loan_id=payload.loan_id,
            type=payload.type,
            amount=payload.amount,
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx

    def list_by_loan(self, db: Session, loan_id: int):
        return db.query(Transaction).filter(Transaction.loan_id == loan_id).all()
