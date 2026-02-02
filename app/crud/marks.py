from sqlalchemy.orm import Session

from app.models import models
from app.schemas import schemas


def get_mark_by_filter(db: Session, filter:schemas.MarkSearchFilter ) -> models.Mark | None:
    """ Get mark filtered by specified params """
    
    mark = db.query(models.Mark) \
                .filter(*filter) \
                .first()
    
    return mark


def create_mark_from_model(db: Session, mark_schema: schemas.MarkCreateModel) -> models.Mark:
    """ Create new mark object """
    
    mark = models.Mark(**mark_schema.model_dump(exclude_unset=True))
    
    db.add(mark)
    db.commit()
    db.refresh(mark)

    return mark

