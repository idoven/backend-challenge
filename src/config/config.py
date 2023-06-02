import os

from database.mongodb_database import DatabaseHandlerMongoDB
from database.volatile_database import DatabaseHandlerVolatile

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if CONNECTION_STRING is None:
    CONNECTION_STRING = "mongodb://localhost:27017/"

DATABASE_NAME = os.getenv("DATABASE_NAME")
if DATABASE_NAME is None:
    DATABASE_NAME = "idoven-challenge"

TESTING = os.getenv("TESTING")
if TESTING is None:
    database = DatabaseHandlerMongoDB(CONNECTION_STRING, DATABASE_NAME)
else:
    database = DatabaseHandlerVolatile()

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    SECRET_KEY = "5856886a40572e88be5551bb12d2742f834bf42495375d95ea3d7261dd44e3db"

ALGORITHM = os.getenv("ALGORITHM")
if ALGORITHM is None:
    ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

