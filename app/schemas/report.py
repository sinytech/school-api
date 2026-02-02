from pydantic import BaseModel
from typing import Optional, Dict, List

from app.schemas.pupils import PupilCreate


# --- Class info for mark stats ---

class ClassInfo(BaseModel):
    average: float
    marks: List[int]

class PupilStatsOut(PupilCreate):
    subject: Dict[str, ClassInfo]

class PupilAllStatsOut(BaseModel):
    pupils: Optional[Dict[int, PupilStatsOut]] = {}
