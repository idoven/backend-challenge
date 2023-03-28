from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities.user import User, get_current_user
from app.domain.constants import pwd_context, users_db


router = APIRouter()


@router.post("/register")
def register_user(user: User, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can create new users")

    if user.username in users_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    users_db[user.username] = user_dict
    return {"message": "User created successfully"}
