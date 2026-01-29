from sqlalchemy.orm import Session
from typing import Optional

from app.core import utils
from app.models import models
from app.schemas import schemas


""" Read user from a database via email """
def get_user_by_email(db: Session, email: str) -> models.User | None:
    user = db.query(models.User) \
            .filter(models.User.email == email) \
            .first()
    
    return user

""" Read user from a database by id """
def get_user_by_id(db: Session, id: int) -> models.User | None:
    user = db.query(models.User) \
                .filter(models.User.id == id) \
                .first()

    return user

""" Find users by search """
def get_all_users_by(db: Session, limit: int = 10, skip: int = 0, search: Optional[str] = "") -> models.User:
    users = db.query(models.User) \
                .filter(models.User.name.contains(search)) \
                .limit(limit) \
                .offset(skip) \
                .all()
    
    return users

""" Create user by schemas.UserCreate schema """
def create_user_with_password_hash(db: Session, user: schemas.UserCreate) -> models.User:

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
