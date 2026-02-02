from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import models
from app.schemas import schemas


def get_pupils_by_owner_id(db: Session, id: int) -> List[models.Pupil]:
    """ Read all pupils by owner id """

    pupils = db.query(models.Pupil) \
            .filter(models.Pupil.user_id == id) \
            .all()
    
    return pupils

def get_pupil_by_school_id(db: Session, school_id: int) -> models.Pupil | None:
    """ Get pupil by school id """

    return db.query(models.Pupil) \
        .filter(models.Pupil.school_id == school_id) \
        .first()


def get_pupil_by_id(db: Session, id: int, owner: Optional[models.User] = None) -> models.Pupil | None:
    """ Get pupil by id """

    filter = [models.Pupil.id == id]
    if owner:
        filter.append(models.Pupil.user_id == owner.id)

    pupil = db.query(models.Pupil) \
                .filter(*filter) \
                .first()
    
    return pupil


def get_pupils_by(db: Session, owner: models.User, limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """ Read all pupils by couple params """

    filter = [models.Pupil.name.contains(search)]
    if owner.id>0:
        filter.append(models.Pupil.user_id == owner.id)

    pupils = db.query(models.Pupil) \
                .filter(**filter) \
                .limit(limit) \
                .offset(skip) \
                .all()

    return pupils


def create_pupil(db: Session, pupil: schemas.PupilCreate, owner: models.User) -> models.Pupil:
    """ Create new pupil model """

    new_pupil = models.Pupil(user_id = owner.id, **pupil.model_dump())
    db.add(new_pupil)
    db.commit()
    db.refresh(new_pupil)

    return new_pupil


def update_pupil(db: Session, pupil: models.Pupil, updated_pupil: schemas.PupilCreate) -> models.Pupil:
    """ Update existing pupil with updated values """
    
    query = db.query(models.Pupil).filter(models.Pupil.id == pupil.id)
    
    query.update(updated_pupil.model_dump(), synchronize_session=False)
    db.commit()

    return query.first()



def delete_pupil_by_id(db: Session, id:int) -> None:
    """ Delete pupil object by id """
    query = db.query(models.Pupil).filter(models.Pupil.id == id)
    query.delete(synchronize_session=False)
    db.commit()