from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated, cast
import jwt
from pwdlib import PasswordHash
import models
from jwt.exceptions import InvalidTokenError
from schema import *
from database import get_db
import os 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_user_from_db(db: Session, username: str):
    return db.query(models.DBUser).filter(models.DBUser.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_from_db(db, username)
    if not user:
        return None
    if not verify_password(password, cast(str, user.hashed_password)):
        return None

    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt 


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "INvalid Credntials",
        headers = {"WWW-Authenticate": "Beare"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credential_exception

    user = get_user_from_db(db, username)
    if user is None:
        raise credential_exception
    return user    

    

def get_current_active_user(current_user: Annotated[models.DBUser, Depends(get_current_user)], db: Session = Depends(get_db)):
    if cast(bool, current_user.disabled):
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user