from typing import Optional

from utilities.record import Record
from models.login_models import UserInDB
from models.ecg_models import ECGResults
from database.database_handler import DatabaseHandler


class DatabaseHandlerVolatile(DatabaseHandler):  # Volatile for testing

    # noinspection SpellCheckingInspection
    def __init__(self):
        self.users = {
            "admin": {
                "username": "admin",
                "full_name": "Administrator",
                "email": "admin@idoven.com",
                "hashed_password": "$2b$12$4M2FCTLRZ7ZtrqIfaOHx0uFPSQ7czthVwFvmb14NGOGvBmbz95.xO",  # Password: password
                "is_admin": True,
            },
            "user1": {
                "username": "user1",
                "full_name": "User McUsername",
                "email": "user1@idoven.com",
                "hashed_password": "$2b$12$4M2FCTLRZ7ZtrqIfaOHx0uFPSQ7czthVwFvmb14NGOGvBmbz95.xO",  # Password: password
                "is_admin": False,
            }
        }
        self.records = dict()

    def add_record(self, record_id: int, record: Record):
        self.records[record_id] = record.dict()

    def retrieve_record(self, record_id: int) -> Optional[Record]:
        record_dict = self.records.get(record_id)
        if record_dict is None:
            return None
        return Record(ECGResults(**record_dict.get("result")), record_dict.get("owner"))

    def retrieve_user(self, username: str) -> Optional[UserInDB]:
        user_dict = self.users.get(username)
        if user_dict is None:
            return None
        return UserInDB(**user_dict)

    def add_user(self, username: str, user_data: UserInDB):
        self.users[username] = user_data.dict()
