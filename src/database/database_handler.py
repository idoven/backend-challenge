from typing import Optional

from utilities.record import Record
from models.login_models import UserInDB


class DatabaseHandler:

    def add_record(self, record_id: int, record: Record):
        pass

    def retrieve_record(self, record_id: int) -> Optional[Record]:
        pass

    def retrieve_user(self, username: str) -> Optional[UserInDB]:
        pass

    def add_user(self, username: str, user_data: UserInDB):
        pass
