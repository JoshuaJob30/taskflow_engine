# backend/app/routes/user_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(db, user_data)

@router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
):
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.get_user_by_id(db, user_id)