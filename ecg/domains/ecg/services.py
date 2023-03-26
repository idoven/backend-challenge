from databases import Database

from . import repositories as repo
from .exceptions import EcgNotFoundError, EcgAccessDeniedError
from .models import ECG
from ..admin.models import User


def calculate_zero_crossings(signal: list[int]) -> int:
    return sum(1 for i in range(len(signal) - 1) if signal[i] * signal[i + 1] < 0)


async def get(db: Database, user: User, ecg_id: str) -> ECG:
    ecg = await repo.get(db, ecg_id)
    if ecg is None:
        raise EcgNotFoundError
    if ecg.owner_id != user.id:
        raise EcgAccessDeniedError
    return ecg
