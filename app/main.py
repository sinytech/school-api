from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.main import api_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router) # , prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Hello World"}

