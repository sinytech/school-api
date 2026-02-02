from datetime import datetime

from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import models
from app.schemas import schemas
from app.core import utils
from app.crud import classes as crud_class, pupils as crud_pupils, marks as crud_marks
from app.services import marks as service_mark


def get_pupil_marks_stats(db: Session, pupil: models.Pupil) -> schemas.PupilStatsOut:
    """ Create statistics for pupil for current quarter """
    
    # ToDo: add quarter selection

    marks = db.query(models.Mark) \
                .join(models.Class) \
                .filter(models.Mark.pupil_id == pupil.id) \
                .order_by(models.Class.title.asc(), models.Mark.mark_date.asc()) \
                .all()
    
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

        res[m]["average"]=f"{avg:.2f}";

    return schemas.PupilStatsOut(**pupil.__dict__, subject=res)


def get_pupil_marks_all_stats(db: Session, owner: models.User )-> schemas.PupilAllStatsOut:
    """ Create marks stats for all owner's pupils """

    pupils = crud_pupils.get_pupils_by_owner_id(db, owner.id)

    result = {}
    for p in pupils:
        result[p.id] = get_pupil_marks_stats(db, p)

    return schemas.PupilAllStatsOut(pupils=result)


def parse_pupil_marks(db: Session, pupil: models.Pupil, data: schemas.MarkCreate) -> schemas.MarkCreateOut:
    """ Parse and add pupil marks from input data """
    
    new_marks_creted = 0

    for subject in data.marks:
        for date in data.marks[subject]:

            subj = crud_class.get_class_or_create(db, subject)

            mark, notes = utils.parse_mark_data(data.marks[subject][date])
            mark_date = datetime.strptime(date, "%d.%m.%y")

            mark_value=-2
            mark_value_ref=''

            if mark=='':
                mark_value=-1
            
            if isinstance(mark, str) and mark:
                if len(mark.split("/"))==2:
                    mark_value, mark_value_ref = mark.split("/")
                else:
                    mark_value = int(mark)

            filter = [
                models.Mark.class_id == subj.id,
                models.Mark.pupil_id == pupil.id,
                models.Mark.quarter == data.quarter,
                models.Mark.mark_date == mark_date
            ]

            old_mark = crud_marks.get_mark_by_filter(db, filter=filter)
            
            if not old_mark:
                mark_value_schema = schemas.MarkCreateModel(
                    class_id=subj.id,
                    pupil_id=pupil.id,
                    mark_date=mark_date,
                    notes=notes,
                    quarter = data.quarter,
                )

                new_mark_ref=None
                if mark_value_ref != '':
                    # add ref mark
                    mark_value_schema.mark=mark_value_ref
                    new_mark_ref=crud_marks.create_mark_from_model(db, mark_value_schema)
                    mark_value_schema.mark_ref_id = new_mark_ref.id
                    new_marks_creted+=1

                # add base mark
                mark_value_schema.mark=mark_value
                crud_marks.create_mark_from_model(db, mark_value_schema)
                
                new_marks_creted+=1
            else:
                if old_mark.mark != mark_value:
                    # ToDo: update marks
                    print(f"ToDo: handle mark changes...")
                    pass

            print(f"Subject: {subj.title}, date: {date}: {data.marks[subject][date]} -- mark: {mark_value} | note: {notes}")

    return schemas.MarkCreateOut(new_marks = new_marks_creted)
