import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
import bcrypt
from dotenv import load_dotenv
from app.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# OAuth2PasswordBearer, token will be retrieved from the header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Create JWT token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Creates an access token with the provided data and expiration time.
    
    - `data`: Dictionary containing the claims to encode in the token.
    - `expires_delta`: Optional timedelta to specify token expiration. If not provided, defaults to the global setting.
    
    Returns a JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(token: str) -> dict:
    """
    Verifies the provided JWT token and decodes it.

    - `token`: The JWT token to be decoded.

    Returns the decoded token payload if valid, otherwise returns an empty dictionary.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return {}

# Retrieve and verify token from header
def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Retrieves the current user from the JWT token.

    - `token`: The JWT token from the request header.

    Returns the decoded user payload if the token is valid, otherwise raises an HTTPException with status 401.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
