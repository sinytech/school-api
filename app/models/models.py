from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    is_active = Column(Boolean, nullable = False, server_default='TRUE')

    name = Column(String, nullable = False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Pupil(Base):
    __tablename__ = 'pupils'

    id = Column(Integer, primary_key = True, nullable = False)
    school_id = Column(Integer, nullable = False)
    user_id = Column(Integer, ForeignKey(
                            "users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable = False)
    form = Column(String, nullable = False)
    year =  Column(Integer, nullable = False)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    user = relationship("User")


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key = True, nullable = False)
    pupil_id = Column(Integer, ForeignKey(
                            "pupils.id", ondelete="CASCADE"), nullable=False)

    class_id = Column(Integer, ForeignKey(
                            "classes.id", ondelete="CASCADE"), nullable=False)
    mark = Column(Integer, nullable = False)
    mark_ref_id = Column(Integer, ForeignKey(
                            "marks.id", ondelete="CASCADE"), nullable=True)

    published_at = Column(TIMESTAMP(timezone=True), nullable = True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    pupil   = relationship("Pupil")
    cls     = relationship("Class")
    mark_ref = relationship("Mark", remote_side=[id], backref='ref_marks')


