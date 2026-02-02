from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core import oauth2
from app.db.database import get_db

from app.schemas import users as schema_users
from app.crud import users as crud_user, pupils as crud_pupils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schema_users.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    users = crud_user.get_all_users_by(db, search= search, limit = limit, skip = skip)
    return users


@router.get("/me", response_model=schema_users.UserOut)
def get_users_me(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    user = crud_user.get_user_by_id(db, id=current_user.id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema_users.UserOut)
def create_user(user: schema_users.UserCreate, db: Session = Depends(get_db)):

    new_user = crud_user.create_user_with_password_hash(db, user)

    return new_user


@router.get('/{id}/pupils', response_model=schema_users.UserPupils)
def get_users_pupils(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = crud_user.get_user_by_id(db, id=id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    pupils = crud_pupils.get_pupils_by_owner_id(db, user.id)
    
    output = schema_users.UserPupils(**user.__dict__, pupils=pupils)
    return output
