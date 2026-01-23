from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pytest import Session
# from . import models
from . import database

# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


# , response_model=schemas.Users
@app.get('/test')
def users_list(db: Session=Depends(database.get_db)):
    return {"result": "success"}
