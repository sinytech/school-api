from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import database
from app.schemas import schemas
from app.models import models
from app.crud import users as crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login', refreshUrl='refresh')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def create_refresh_token(data: dict):
    to_encode = data.copy()
    
    # 1. Set longer expiration
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 2. Add 'type' to prevent Token Substitution attacks
    to_encode.update({
        "exp": expire,
        "type": "refresh" 
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("type")
        
        if token_type != "refresh" or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired or invalid")
    
    return user_id


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = crud_user.get_user_by_id(db, token.id)
    return user

