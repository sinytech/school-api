from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.schemas import marks, pupils
from app.db.database import get_db
from app.core import oauth2
from app.crud import pupils as crud_pupils
from app.services import marks as service_marks

router = APIRouter(
    prefix="/marks",
    tags=['Marks']
)

@router.post("/submit", status_code=status.HTTP_201_CREATED, response_model=marks.MarkCreateOut)
def create_marks(data: marks.MarkCreate, db: Session = Depends(get_db), owner: int = Depends(oauth2.get_current_user)):

    pupil = crud_pupils.get_pupil_by_school_id(db, data.school_id)

    if not pupil:
        pupul_schema = pupils.PupilCreate(
                            school_id=data.school_id,
                            name=data.name,
                            form='0 Z',
                            year=0
                        )
        pupil = crud_pupils.create_pupil(db, pupil=pupul_schema, owner=owner)
    
    if pupil.user_id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to perform requested action")

    
    return service_marks.parse_pupil_marks(db, pupil=pupil, data=data)
