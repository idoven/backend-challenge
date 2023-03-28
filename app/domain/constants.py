# User database
from fastapi.security import HTTPBearer, HTTPBasic
from passlib.context import CryptContext


users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$mqhJ0.qg/mjKxgzOhkAbHONhDW1Zg0bZvKjzM9TtTctTtRFljK0yS",  # password: adminpass
        "is_admin": True
    },
    "test": {
        "username": "test",
        "password": "$2b$12$mqhJ0.qg/mjKxgzOhkAbHONhDW1Zg0bZvKjzM9TtTctTtRFljK0yS", # password: adminpass
        "is_admin": False
    }
}

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
