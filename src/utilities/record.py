from models.ecg_models import ECGResults


class Record:
    def __init__(self, result: ECGResults, username: str):
        self.result = result
        self.owner = username

    def dict(self):
        return {"record_id": self.result.id,
                "owner": self.owner,
                "result": self.result.dict()}
