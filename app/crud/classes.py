from sqlalchemy.orm import Session
from app.models import models


""" Get class by title """
def get_class_by_title(db:Session, class_title: str) -> models.Class | None:

    return db.query(models.Class) \
                .filter(models.Class.title == class_title) \
                .first()


""" Create new class object """
def create_class(db:Session, class_title: str) -> models.Class:
    my_class = models.Class(title=class_title)
    db.add(my_class)
    db.commit()
    db.refresh(my_class)

    return my_class


""" Return requested class by title (create if neccessary) """
def get_class_or_create(db:Session, class_title: str) -> models.Class:
    my_class = get_class_by_title(db, class_title)
    
    if not my_class:
        my_class = create_class(db, class_title)

    return my_class
