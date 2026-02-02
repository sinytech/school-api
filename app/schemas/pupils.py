from pydantic import BaseModel

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


