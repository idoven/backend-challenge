from fastapi import APIRouter
from app.api.v1.endpoints import login, register, data

v1_router = APIRouter()

v1_router.include_router(data.router, prefix='/ecg', tags=['data'])
v1_router.include_router(login.router, prefix='/user', tags=['login'])
v1_router.include_router(register.router, prefix='/user', tags=['register'])

