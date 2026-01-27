from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas import schemas
from ..database import get_db
from ..models import models
from .. import oauth2

router = APIRouter(
    prefix="/pupils",
    tags=['Pupils']
)

@router.get("/", response_model=List[schemas.PupilOut])
def get_pupils(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    pupils = db.query(models.Pupil) \
                .filter(models.Pupil.name.contains(search)) \
                .limit(limit) \
                .offset(skip) \
                .all()

    return pupils


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PupilOut)
def create_pupil(pupil: schemas.PupilCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_pupil = models.Pupil(user_id = current_user.id, **pupil.model_dump())
    db.add(new_pupil)
    db.commit()
    db.refresh(new_pupil)

    return new_pupil


@router.put("/{id}", response_model=schemas.PupilOut)
def update_pupil(id: int, updated_post: schemas.PupilCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    pupil_query = db.query(models.Pupil).filter(models.Pupil.id == id)
    pupil = pupil_query.first()

    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pupil with id: {id} does not exist")

    print(f"pupil.id = {pupil.user_id}, current user = {current_user.id}")
    if pupil.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    pupil_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return pupil_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pupil(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    pupil_query = db.query(models.Pupil).filter(models.Pupil.id == id)
    pupil = pupil_query.first()

    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {id} does not exist")

    if pupil.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    pupil_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

