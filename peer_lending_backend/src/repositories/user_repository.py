# Repository class for managing User entities in the database using SQLAlchemy #


from sqlalchemy.orm import Session
from models.users import User
from schemas.user import UserCreate

class UserRepository:
    def create(self, db: Session, payload: UserCreate):
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
