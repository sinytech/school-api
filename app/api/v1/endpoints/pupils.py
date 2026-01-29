from fastapi import  status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas import schemas
from app.db.database import get_db
from app.core import oauth2
from app.models import models
from app.crud import pupils as crud_pupils
from app.services import marks as services_mark

router = APIRouter(
    prefix="/pupils",
    tags=['Pupils']
)

@router.get("/", response_model=List[schemas.PupilOut])
def get_pupils(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    pupils = crud_pupils.get_pupils_by(db=db, owner = user, limit=limit, skip=skip, search=search)

    return pupils


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PupilOut)
def create_pupil(pupil: schemas.PupilCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_pupil = crud_pupils.create_pupil(db, pupil=pupil, owner=current_user)

    return new_pupil


@router.put("/{id}", response_model=schemas.PupilOut)
def update_pupil(id: int, updated_pupil: schemas.PupilCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    pupil = crud_pupils.get_pupil_by_id(db, id)

    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pupil with id: {id} does not exist")

    print(f"pupil.id = {pupil.user_id}, current user = {current_user.id}")
    if pupil.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    return crud_pupils.update_pupil(db, pupil, updated_pupil)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pupil(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    pupil = crud_pupils.get_pupil_by_id(db, id)
    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {id} does not exist")

    if pupil.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    crud_pupils.delete_pupil_by_id(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}/stats", response_model=schemas.PupilStatsOut)
def get_pupil_stats(id: int, db: Session = Depends(get_db)):

    pupil = crud_pupils.get_pupil_by_id(db, id)

    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {id} does not exist")

    return services_mark.get_pupil_marks_stats(db, pupil=pupil)


@router.get("/stats", response_model=schemas.PupilAllStatsOut)
def get_pupil_all_stats(db: Session = Depends(get_db), owner: models.User = Depends(oauth2.get_current_user)):

    return services_mark.get_pupil_marks_all_stats(db, owner=owner)
