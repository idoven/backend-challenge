from datetime import datetime

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ecg.api.dependencies.auth import get_current_user
from ecg.api.dependencies.database import get_db
from ecg.domains.admin.models import User
from ecg.domains.ecg.exceptions import UniqueEcgError
from ecg.domains.ecg.models import ECG, LeadTypeEnum

from ecg.domains.ecg import services as ecg_services
from ecg.domains.ecg import repositories as ecg_repo
from ecg.domains.ecg import exceptions as ecg_exceptions

router = APIRouter()


# In schemas
class LeadIn(BaseModel):
    name: LeadTypeEnum
    sample_size: int | None = None
    signal: list[int]


class EcgIn(BaseModel):
    id: str
    date: datetime
    leads: list[LeadIn]


# Add user end_point
@router.post("/ecg")
async def add_ecg(
    ecg: EcgIn,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
) -> dict[str, str]:
    ecg_model = ECG(**ecg.dict(), owner_id=user.id)
    try:
        await ecg_repo.create(db, ecg_model)
    except UniqueEcgError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ECG already exists",
        )
    return {"message": "ECG successfully added"}


class LeadOut(BaseModel):
    name: str
    crossings: int


class EcgOut(BaseModel):
    id: str
    leads: list[LeadOut]


@router.get("/ecg/{ecg_id}")
async def get_ecg(
    ecg_id: str,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
) -> EcgOut:
    try:
        ecg_model = await ecg_services.get(db, user, ecg_id)
    except ecg_exceptions.EcgNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ECG not found",
        )
    except ecg_exceptions.EcgAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    leads = [
        LeadOut(
            name=lead.name, crossings=ecg_services.calculate_zero_crossings(lead.signal)
        )
        for lead in ecg_model.leads
    ]

    return EcgOut(id=ecg_id, leads=leads)
