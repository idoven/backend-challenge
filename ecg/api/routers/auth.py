from datetime import timedelta

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ecg.api.dependencies.auth import create_access_token
from ecg.api.dependencies.database import get_db
from ecg.domains.admin.exceptions import UserAccessDeniedError
from ecg.domains.admin.services import authenticate_user

router = APIRouter()


# Token endpoint
@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)
):
    try:
        user = await authenticate_user(form_data.username, form_data.password, db)
    except UserAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
