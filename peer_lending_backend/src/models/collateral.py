# SQL Alchemy model for the Collateral table #

from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from peer_lending_backend.src.db.database import Base

class Collateral(Base):
    __tablename__ = "collateral"

    collateral_id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("users.user_id"))
    type = Column(String(100))
    value = Column(DECIMAL(10, 2))
    verification_status = Column(String(50))
    created_at = Column(DateTime)

    borrower = relationship("User")
