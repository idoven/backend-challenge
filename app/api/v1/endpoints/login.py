from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from datetime import timedelta
from app.domain.constants import basic_scheme, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.entities.user import authenticate_user, create_access_token

router = APIRouter()


@router.post("/login")
def login_user(credentials: HTTPBasicCredentials = Depends(basic_scheme)):

    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
