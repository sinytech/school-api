from turtle import title
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from .models import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error occured: {e}")

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Парсим строку по 8|note
def parse_mark_data(data):
    # partition делит строку по первому встречному '|'
    mark, separator, note = data.partition('|')
    
    # Убираем лишние пробелы, если они есть
    mark = mark.strip()
    note = note.strip()
    
    # Если оценки нет (случай 2), mark будет пустой строкой
    # Если заметки нет (случай 1), note будет пустой строкой
    return mark, note



def get_class_or_create(db:Session, class_title: str) -> models.Class:
    my_class = db.query(models.Class).filter(models.Class.title == class_title).first()
    if not my_class:
        my_class = models.Class(title=class_title)
        db.add(my_class)
        db.commit()
        db.refresh(my_class)

    return my_class

