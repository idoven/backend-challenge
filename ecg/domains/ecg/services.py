from databases import Database

from ecg.domains.admin.models import User

from ..admin.services import is_admin
from . import repositories as repo
from .exceptions import EcgAccessDeniedError, EcgNotFoundError
from .models import ECG


def calculate_zero_crossings(signal: list[int]) -> int:
    zero_crossings = 0
    for i in range(len(signal) - 1):
        if (signal[i] >= 0 and signal[i + 1] < 0) or (
            signal[i] <= 0 and signal[i + 1] > 0
        ):
            zero_crossings += 1
    return zero_crossings


async def get(db: Database, user: User, ecg_id: str) -> ECG:
    ecg = await repo.get(db, ecg_id)
    if ecg is None:
        raise EcgNotFoundError
    if ecg.owner_id != user.id:
        raise EcgAccessDeniedError
    if is_admin(user):
        raise EcgAccessDeniedError
    return ecg


async def create(db: Database, user: User, ecg: ECG) -> None:
    if is_admin(user):
        raise EcgAccessDeniedError
    await repo.create(db, ecg)
