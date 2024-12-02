from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.domains.users.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def get_by_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()

        return user

    def get_all(self, skip: int = 0, limit: int = 10):
        users = self.db.query(User).offset(skip).limit(limit).all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No users found"
            )

        return users

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully."}
