from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import HTTPBearer
from app.domain.constants import SECRET_KEY, ALGORITHM, users_db, bearer_scheme, pwd_context
from datetime import datetime, timedelta


class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False
    
    class Config:
        schema_extra: dict = {
            'example': {
                'username': 'john',
                'password':'password',
                'is_admin': False
            }
        }


# JWT functions
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        token_data = {"username": username}
        return token_data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)


# Dependency to get current user
def get_current_user(credentials: HTTPBearer = Depends(bearer_scheme)):
    token_data = decode_access_token(credentials.credentials)
    user = get_user(token_data["username"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    return user


# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        #return get_user("admin")
        #return get_user("test")
        return False
    if not verify_password(password, user.password):
        return False
    return user



