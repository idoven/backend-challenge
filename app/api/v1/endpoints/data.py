from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities.user import User, get_current_user
from app.domain.entities.data import Data

router = APIRouter()

# Data storage
data_storage = {}


@router.post("/send_data")
def save_data(data: Data, user: User = Depends(get_current_user)):
    if user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin users are not allowed to save data")
    data_storage[user.username] = data.data
    return {"message": "Data saved successfully"}


@router.get("/get_data")
def get_data(user: User = Depends(get_current_user)):
    if user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin users are not allowed to get data")
    if user.username not in data_storage:
        return {"message": "No data found for the user"}
    return {"data": Data.check_values(data_storage[user.username])}
