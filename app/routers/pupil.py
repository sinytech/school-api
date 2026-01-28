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


@router.get("/{id}/stats", response_model=schemas.PupilStatsOut)
def get_pupil_stats(id: int, db: Session = Depends(get_db)):
    pupil = db.query(models.Pupil).filter(models.Pupil.id == id).first()

    if pupil == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {id} does not exist")

    marks = db.query(models.Mark) \
                .join(models.Class) \
                .filter(models.Mark.pupil_id == pupil.id) \
                .order_by(models.Class.title, models.Mark.mark_date) \
                .all()
    
    # print(f"For pupil id {id} ({pupil.name}) there are following marks: {len(marks)}")

    res = {}
    for m in marks:
        if not m.cls.title in res:
            res[m.cls.title] = {
                "average": 0,
                "marks": []
            }
        if m.mark>0:
            res[m.cls.title]["marks"].append(m.mark)    

    for m in res:
        avg = 0
        if len(res[m]["marks"]):
            avg = sum(res[m]["marks"]) / len(res[m]["marks"])

        res[m]["average"]=avg;

    return schemas.PupilStatsOut(**pupil.__dict__, subject=res)


@router.get("/stats", response_model=schemas.PupilAllStatsOut)
def get_pupils_all_stats(db: Session = Depends(get_db)):
    pupils = db.query(models.Pupil).filter(models.Pupil.user_id == 5).all()

    for p in pupils:
        # ToDo: re-use business-logic
        pass

    return schemas.PupilAllStatsOut()