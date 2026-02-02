from sqlalchemy.orm import Session
from app.models import models


def get_class_by_title(db:Session, class_title: str) -> models.Class | None:
    """ Get class by title """

    return db.query(models.Class) \
                .filter(models.Class.title == class_title) \
                .first()


def create_class(db:Session, class_title: str) -> models.Class:
    """ Create new class object """

    my_class = models.Class(title=class_title)
    db.add(my_class)
    db.commit()
    db.refresh(my_class)

    return my_class


def get_class_or_create(db:Session, class_title: str) -> models.Class:
    """ Return requested class by title (create if neccessary) """

    my_class = get_class_by_title(db, class_title)
    
    if not my_class:
        my_class = create_class(db, class_title)

    return my_class
