from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

# from .. import models, schemas, oauth2
from ..schemas import schemas
from ..database import get_db
from ..models import models


router = APIRouter(
    prefix="/pupils",
    tags=['Pupils']
)

@router.get("/", response_model=List[schemas.PupilOut])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
def get_pupils(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    pupils = db.query(models.Pupil) \
                .filter(models.Pupil.name.contains(search)) \
                .limit(limit) \
                .offset(skip) \
                .all()

    return pupils
