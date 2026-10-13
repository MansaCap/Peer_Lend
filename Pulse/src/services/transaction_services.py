# Service class for managing transactions, including recording and listing transactions for a specific loan. #

from sqlalchemy.orm import Session
from repositories.transaction_repository import TransactionRepository
from schemas.transaction import TransactionCreate

class TransactionService:
    def __init__(self):
        self.repo = TransactionRepository()

    def record(self, db: Session, payload: TransactionCreate):
        return self.repo.create(db, payload)

    def list_for_loan(self, db: Session, loan_id: int):
        return self.repo.list_by_loan(db, loan_id)
