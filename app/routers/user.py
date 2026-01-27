from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas import schemas
from ..database import get_db
from ..models import models
from .. import oauth2, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    users = db.query(models.User) \
                .filter(models.User.name.contains(search)) \
                .limit(limit) \
                .offset(skip) \
                .all()

    return users


@router.get("/me", response_model=schemas.UserOut)
def get_users_me(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User) \
                .filter(models.User.id == current_user.id) \
                .first()
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}/pupils', response_model=schemas.UserPupils)
def get_users_pupils(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    pupils = db.query(models.Pupil) \
                .filter(models.Pupil.user_id == user.id) \
                .all()
    
    output = schemas.UserPupils(**user.__dict__, pupils=pupils)
    return output
