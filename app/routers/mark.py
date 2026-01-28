from datetime import datetime
from weakref import ref
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from pytest import Mark
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas import schemas
from ..database import get_db
from ..models import models
from .. import oauth2
from ..utils import get_class_or_create
from ..utils import parse_mark_data

router = APIRouter(
    prefix="/marks",
    tags=['Marks']
)

@router.post("/submit", status_code=status.HTTP_201_CREATED, response_model=schemas.MarkCreateOut)
def create_marks(data: schemas.MarkCreate, db: Session = Depends(get_db)):

    print(f"Input data = {data}")
    # ToDo: add validation for the logged in User

    # get pupil
    pupil = db.query(models.Pupil).filter(models.Pupil.school_id == data.school_id).first()
    if not pupil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {data.school_id} does not exist")
    
    new_marks_creted = 0

    for subject in data.marks:
        for date in data.marks[subject]:
            subj = get_class_or_create(db, subject)

            mark, notes = parse_mark_data(data.marks[subject][date])
            mark_date = datetime.strptime(date, "%d.%m.%y")

            mark_value=0
            mark_value_ref=''

            if mark=='':
                mark_value=-1
            
            if mark!=-1 and type(mark) == str:
                if len(mark.split("/"))==2:
                    print(f"mark={mark}")
                    mark_value, mark_value_ref = mark.split("/")
                    print(f"Ref Mark Value is not supported yet mark={mark_value} mark_value_ref = {mark_value_ref}")

            old_mark = db.query(models.Mark).filter(
                                models.Mark.class_id==subj.id, models.Mark.pupil_id == pupil.id,
                                # models.Mark.mark==mark_value, models.Mark.notes==notes,
                                models.Mark.quarter == data.quarter,
                                models.Mark.mark_date == mark_date
                        ).first()
            
            if not old_mark:
                new_mark_ref=None
                if mark_value_ref != '':
                    new_mark_ref = models.Mark(cls=subj, pupil = pupil, 
                                    mark=mark_value_ref, notes=notes,
                                    quarter = data.quarter,
                                    mark_date = mark_date,
                                    )
                    db.add(new_mark_ref)
                    db.commit()
                    db.refresh(new_mark_ref)
                    new_marks_creted+=1

                new_mark = models.Mark(cls=subj, pupil = pupil, 
                                    mark=mark_value, notes=notes,
                                    quarter = data.quarter,
                                    mark_date = mark_date,
                                    mark_ref = new_mark_ref
                                    )
                db.add(new_mark)
                db.commit()
                db.refresh(new_mark)
                new_marks_creted+=1
            else:
                if old_mark.mark != mark_value:
                    # ToDo: update marks
                    print(f"ToDo: handle mark changes...")
                    pass

            print(f"Subject: {subj.title}, date: {date}: {data.marks[subject][date]} -- mark: {mark_value} | note: {notes}")

    out = schemas.MarkCreateOut(new_marks = new_marks_creted)
    return out
