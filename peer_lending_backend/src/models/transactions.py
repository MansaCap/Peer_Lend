# SQL Alchemy model for the Transaction table #
# This table records all financial transactions related to loans, including disbursements, repayments, and fees.

from sqlalchemy import Column, Integer, DECIMAL, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from peer_lending_backend.src.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.loan_id"))
    type = Column(String(50))  # disbursement, repayment, fee, etc.
    amount = Column(DECIMAL(10, 2))
    created_at = Column(DateTime)

    loan = relationship("Loan")
