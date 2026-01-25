from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pytest import Session
from . import database
from .routers import pupil, user

app = FastAPI()
app.include_router(pupil.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


# , response_model=schemas.Users
@app.get('/test')
def users_list(db: Session=Depends(database.get_db)):
    return {"result": "success"}


# --- Sample database request ---
# date=19.01.26
# pupil_id=1231122
# marks = [
    # { class: "Math", mark: "10\6" }
# ]
# End of ignore section