from fastapi import APIRouter

from .endpoints import auth, marks, utils, users, pupils

api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(utils.router)
api_router.include_router(users.router)
api_router.include_router(pupils.router)
api_router.include_router(marks.router)
