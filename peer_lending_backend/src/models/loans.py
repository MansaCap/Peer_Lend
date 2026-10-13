# SQL Alchemy model for the Loan table #

from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from peer_lending_backend.src.db.database import Base

class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(DECIMAL(10, 2))
    interest_rate = Column(DECIMAL(5, 2))
    term_months = Column(Integer)
    status = Column(String(50))
    created_at = Column(DateTime)

    borrower = relationship("User")
