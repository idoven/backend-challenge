from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from config.config import database, SECRET_KEY, ALGORITHM
from models.login_models import UserInDB, TokenData, UserRegistrationForm
from database.database_handler import DatabaseHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: DatabaseHandler, username: str):
    return db.retrieve_user(username)


def authenticate_user(db: DatabaseHandler, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def register_user(form: UserRegistrationForm):
    if database.retrieve_user(form.username):
        raise HTTPException(status_code=422, detail=f"Username '{form.username}' is already taken")

    user = UserInDB(username=form.username,
                    email=form.email,
                    full_name=form.full_name,
                    organization=form.organization,
                    is_admin=form.is_admin,
                    hashed_password=get_password_hash(form.password))
    database.add_user(form.username, user)
