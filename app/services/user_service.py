from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

# CRUD
def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()

def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        is_active=payload.is_active if payload.is_active is not None else True,
        is_superuser=payload.is_superuser if payload.is_superuser is not None else False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, db_user: User, payload: UserUpdate) -> User:
    if payload.username is not None:
        db_user.username = payload.username
    if payload.email is not None:
        db_user.email = payload.email
    if payload.full_name is not None:
        db_user.full_name = payload.full_name
    if payload.is_active is not None:
        db_user.is_active = payload.is_active
    if payload.is_superuser is not None:
        db_user.is_superuser = payload.is_superuser
    if payload.password:
        db_user.hashed_password = hash_password(payload.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User) -> None:
    db.delete(db_user)
    db.commit()
