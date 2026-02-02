from typing import List
from pydantic import BaseModel, EmailStr

from app.schemas.pupils import PupilOut


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

# --- User with Pupils Schema ---

class UserPupils(UserBase):
    id: int
    pupils: List[PupilOut]

