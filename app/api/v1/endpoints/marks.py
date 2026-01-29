from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.db.database import get_db

from app.crud import pupils as crud_pupils
from app.services import marks as service_marks

router = APIRouter(
    prefix="/marks",
    tags=['Marks']
)

@router.post("/submit", status_code=status.HTTP_201_CREATED, response_model=schemas.MarkCreateOut)
def create_marks(data: schemas.MarkCreate, db: Session = Depends(get_db)):

    # ToDo: add validation for the logged in User
    pupil = crud_pupils.get_pupil_by_school_id(db, data.school_id)

    if not pupil:
        # ToDo: handle the case... create new pupil under logged user = owner
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pupil with id: {data.school_id} does not exist")
    
    return service_marks.parse_pupil_marks(db, pupil=pupil, data=data)
