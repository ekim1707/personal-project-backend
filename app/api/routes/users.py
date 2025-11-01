from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_existing_user_or_404
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db_dep),
):
    return user_service.list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db_user: User = Depends(get_existing_user_or_404)):
    return db_user

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db_dep)):
    # Optional: enforce uniqueness here to return 400 instead of DB error
    if user_service.get_user_by_email(db, payload.email):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_service.get_user_by_username(db, payload.username):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Username already taken")

    return user_service.create_user(db, payload)

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db_dep),
    db_user: User = Depends(get_existing_user_or_404),
):
    # If changing email/username, ensure uniqueness
    if payload.email and payload.email != db_user.email:
        if user_service.get_user_by_email(db, payload.email):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Email already registered")
    if payload.username and payload.username != db_user.username:
        if user_service.get_user_by_username(db, payload.username):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Username already taken")

    return user_service.update_user(db, db_user, payload)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db_dep),
    db_user: User = Depends(get_existing_user_or_404),
):
    user_service.delete_user(db, db_user)
    return None
