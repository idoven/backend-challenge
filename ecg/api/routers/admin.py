from databases import Database
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from ecg.api.dependencies.auth import get_current_user
from ecg.api.dependencies.database import get_db
import ecg.domains.admin.services as admin_services
import ecg.domains.admin.exceptions as admin_exceptions
from ecg.domains.admin.models import User

router = APIRouter()


class UserIn(BaseModel):
    email: str
    password: str


@router.post("/users")
async def add_user(
    user_data: UserIn,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    try:
        await admin_services.create_user(
            db=db,
            creator=current_user,
            email=user_data.email,
            password=user_data.password,
        )
    except admin_exceptions.NotUniqueUserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    except admin_exceptions.UserAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add user",
        )
    return {"message": "User added"}


@router.delete("/users/{email}")
async def delete_user(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    try:
        await admin_services.delete_user(db, current_user, email)
    except admin_exceptions.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except admin_exceptions.UserAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this user",
        )
    except admin_exceptions.UserSelfDeletionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't delete yourself",
        )
    return {"message": "User deleted"}
