from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import user_service

def get_db_dep(db: Session = Depends(get_db)) -> Session:
    return db

def get_existing_user_or_404(user_id: int, db: Session = Depends(get_db_dep)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
