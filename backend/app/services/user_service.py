# backend/app/services/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repo
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = user_repo.get_user_by_email(db, user_data.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data.email} already exists",
        )

    return user_repo.create_user(db, user_data)

def get_user_by_id(db: Session, user_id: int) -> User:
    user = user_repo.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist",
        )

    return user

def get_all_users(db: Session) -> list:
    return user_repo.get_all_users(db)