from pydantic import BaseModel, EmailStr, ConfigDict
# from datetime import datetime
from typing import Optional, Dict

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



# --- User with Pupils Schema ---

class UserPupils(UserBase):
    id: int
    pupils: list[PupilOut]


class MarkCreate(BaseModel):
    school_id: int
    quarter: int
    # Dict[название_предмета, Dict[дата, оценка_или_текст]]
    marks: Dict[str, Dict[str, str]]


class MarkCreateOut(BaseModel):
    new_marks: int
    