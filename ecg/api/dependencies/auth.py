from datetime import datetime, timedelta
from typing import Optional

from databases import Database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from ecg.api.dependencies.database import get_db
from ecg.domains.admin.models import User
from ecg.domains.admin import services as admin_services

from ecg.config import settings

# Secret key and algorithm for JWT
SECRET_KEY = settings.jwt_key
ALGORITHM = "HS256"

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


InvalidCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
)


# Get current user
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise InvalidCredentialsError
        user = await admin_services.get_user(db, email)
        if user is None:
            raise InvalidCredentialsError
        return user
    except jwt.PyJWTError:
        raise InvalidCredentialsError
