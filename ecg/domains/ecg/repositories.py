from asyncpg import UniqueViolationError
from databases import Database

from ecg.domains.ecg.exceptions import UniqueEcgError
from ecg.domains.ecg.models import ECG, Lead
from ecg.sql.ecg import (
    CREATE_ECG_QUERY,
    CREATE_LEAD_QUERY,
    GET_ECG_BY_ID_QUERY,
    GET_LEAD_BY_ECG_ID_QUERY,
)


async def create(db: Database, ecg: ECG):
    values = {"id": ecg.id, "owner_id": ecg.owner_id, "date": ecg.date}
    try:
        await db.execute(CREATE_ECG_QUERY, values)
    except UniqueViolationError:
        raise UniqueEcgError
    for lead in ecg.leads:
        await _create_lead(db, lead, ecg.id)


async def _create_lead(db: Database, lead: Lead, ecg_id: str):
    values = {"name": lead.name, "ecg_id": ecg_id, "signal": lead.signal}
    await db.execute(CREATE_LEAD_QUERY, values)


async def get(db: Database, ecg_id: str) -> ECG | None:
    values = {"ecg_id": ecg_id}
    ecg_row = await db.fetch_one(GET_ECG_BY_ID_QUERY, values)

    if ecg_row is None:
        return None

    leads = await _get_leads_by_ecg_id(db, ecg_id)

    return ECG(
        id=ecg_row["id"],
        owner_id=ecg_row["owner_id"],
        date=ecg_row["date"],
        leads=leads,
    )


async def _get_leads_by_ecg_id(db: Database, ecg_id: str) -> list[Lead]:
    values = {"ecg_id": ecg_id}
    lead_rows = await db.fetch_all(GET_LEAD_BY_ECG_ID_QUERY, values)

    leads = [Lead(name=row["name"], signal=row["signal"]) for row in lead_rows]
    return leads
