from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

# --- Pupil Schemas ---
class PupilBase(BaseModel):
    id: int
    user_id: int
    school_id: int
    name: str
    form: str
    year: int


class PupilCreate(BaseModel):
    school_id: int
    name: str
    form: str
    year: int

class PupilOut(PupilBase):
    class Config:
        from_attributes = True


# --- Class info for mark stats ---

class ClassInfo(BaseModel):
    average: float
    marks: List[int]

class PupilStatsOut(PupilCreate):
    subject: Dict[str, ClassInfo]

class PupilAllStatsOut(BaseModel):
    pupils: Optional[Dict[int, PupilStatsOut]] = {}

# --- User with Pupils Schema ---

class UserPupils(UserBase):
    id: int
    pupils: List[PupilOut]


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
