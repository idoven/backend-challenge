from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class LeadTypeEnum(str, Enum):
    I = "I"  # noqa: E741
    II = "II"
    III = "III"
    aVR = "aVR"
    aVL = "aVL"
    aVF = "aVF"
    V1 = "V1"
    V2 = "V2"
    V3 = "V3"
    V4 = "V4"
    V5 = "V5"
    V6 = "V6"


class Lead(BaseModel):
    name: LeadTypeEnum
    signal: list[int]


class ECG(BaseModel):
    id: str
    owner_id: UUID
    date: datetime
    leads: list[Lead]
