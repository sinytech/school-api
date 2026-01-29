from sqlalchemy.orm import Session

from app.models import models
from app.schemas import schemas


""" Get mark filtered by specified params """
def get_mark_by_filter(db: Session, filter:schemas.MarkSearchFilter ) -> models.Mark | None:
    
    mark = db.query(models.Mark) \
                .filter(*filter) \
                .first()
    
    return mark


""" Create new mark object """
def create_mark_from_model(db: Session, mark_schema: schemas.MarkCreateModel) -> models.Mark:
    
    print(f"Input values {mark_schema.model_dump(exclude_unset=True)}")
    mark = models.Mark(**mark_schema.model_dump(exclude_unset=True))
    
    db.add(mark)
    db.commit()
    db.refresh(mark)

    return mark

