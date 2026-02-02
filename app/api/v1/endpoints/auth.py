import json
from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import oauth2
from app.db import database

from app.schemas import schemas
from app.core import utils

from app.crud import users as crud_users

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = crud_users.get_user_by_email(db, user_credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create & return a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})
    
    content = json.dumps({"access_token": access_token, "token_type": "bearer"})
    
    response = Response(content=content, media_type="application/json")
    response.set_cookie(
                            key="refreshtoken",
                            value=refresh_token, 
                            httponly=True,   # JS cannot steal it (XSS protection)
                            secure=True,     # Only sent over HTTPS
                            samesite="lax"   # CSRF protection
                        )
    return response


@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(database.get_db)):
    # 1. Extract refresh token from Secure Cookie
    refresh_token = request.cookies.get("refreshtoken")
    
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    # 2. Validate Refresh Token
    user_id = oauth2.validate_refresh_token(refresh_token)

    # 3. Verify user still exists in DB
    user = crud_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # 4. Generate NEW Access Token
    new_access_token = oauth2.create_access_token(data={"user_id": user.id})

    return { "access_token": new_access_token, "token_type": "bearer" }
