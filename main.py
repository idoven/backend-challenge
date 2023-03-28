from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPBasic
from passlib.context import CryptContext
from app.core.config import settings
from app.api.router import v1_router


app = FastAPI()
app.include_router(v1_router, prefix=settings.API_PREFIX)

# Data storage
data_storage = {}

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security schemes
bearer_scheme = HTTPBearer()
basic_scheme = HTTPBasic()

# JWT settings
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
