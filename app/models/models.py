from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable = False)
    school_id = Column(Integer, nullable = False)
    name = Column(String, nullable = False)
    form = Column(String, nullable = False)
    year =  Column(Integer, nullable = False)

