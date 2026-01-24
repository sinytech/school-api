from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional

# from pydantic.types import conint


class PupilBase(BaseModel):
    id: int
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


