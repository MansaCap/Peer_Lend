# SQL Alchemy model for the User table #
from sqlalchemy import Column, Integer, String, DateTime

from peer_lending_backend.src.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime)
