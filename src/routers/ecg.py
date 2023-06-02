from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status

from config.config import database
from processor.basic_processor import ECGProcessor
from models.ecg_models import ECGData
from models.login_models import User
from utilities.login_utils import get_current_user

router = APIRouter()
processor = ECGProcessor(database)


@router.get("/get/{requested_id}")
async def retrieve(requested_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin users cannot perform this operation",
        )

    result = database.retrieve_record(requested_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Result ID {requested_id} does not exist",
        )

    if result.owner != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to access these results",
        )

    return {"result": result.result}


@router.post("/submit")
async def ingest_ecg(item: ECGData, current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin users cannot perform this operation",
        )

    await processor.process_ecg(item, current_user.username)

    return {"message": f"Accepted input, results will be available with id {item.id}"}
