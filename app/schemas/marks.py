from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

class MarkCreate(BaseModel):
    school_id: int  # pupil school_id
    quarter: int
    name: str   # pupil name
    # Dict[название_предмета, Dict[дата, оценка_или_текст]]
    marks: Dict[str, Dict[str, str]]


class MarkCreateOut(BaseModel):
    new_marks: int


class MarkSearchFilter(BaseModel):
    class_id: Optional[int]
    pupil_id: Optional[int]
    mark_date: Optional[datetime]
    quarter: Optional[int]
    notes: Optional[str]

class MarkCreateModel(MarkSearchFilter):
    mark_ref_id: Optional[int] = None
    mark: Optional[int] = 0

