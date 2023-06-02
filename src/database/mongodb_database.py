from pymongo import MongoClient
from typing import Optional

from utilities.record import Record
from models.login_models import UserInDB
from models.ecg_models import ECGResults
from database.database_handler import DatabaseHandler


class DatabaseHandlerMongoDB(DatabaseHandler):  # MongoDB version

    def __init__(self, connection_string: str, database_name: str):
        client = MongoClient(connection_string)
        database = client[database_name]
        self.users = database["users"]
        self.records = database["records"]

    def add_record(self, record_id: int, record: Record):
        record_selector = {"record_id": record_id}
        self.records.update_one(record_selector, {"$set": record.dict()}, upsert=True)

    def retrieve_record(self, record_id: int) -> Optional[Record]:
        record_dict = self.records.find_one({"record_id": record_id})
        if record_dict is None:
            return None
        return Record(ECGResults(**record_dict.get("result")), record_dict.get("owner"))

    def retrieve_user(self, username: str) -> Optional[UserInDB]:
        user_dict = self.users.find_one({"username": username})
        if user_dict is None:
            return None
        return UserInDB(**user_dict)

    def add_user(self, username: str, user_data: UserInDB):
        self.users.insert_one(user_data.dict())
