from datetime import datetime

from pydantic import BaseModel

from ecg.domains.ecg.models import LeadTypeEnum


## ECG
class LeadIn(BaseModel):
    name: LeadTypeEnum
    sample_size: int | None = None
    signal: list[int]


class EcgIn(BaseModel):
    id: str
    date: datetime
    leads: list[LeadIn]


class LeadOut(BaseModel):
    name: str
    crossings: int


class EcgOut(BaseModel):
    id: str
    leads: list[LeadOut]


## Admin
class UserIn(BaseModel):
    email: str
    password: str
