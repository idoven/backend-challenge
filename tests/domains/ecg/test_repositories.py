from datetime import datetime
from uuid import uuid4

import pytest
from asyncpg import UniqueViolationError
from databases import Database

from ecg.domains.ecg.exceptions import UniqueEcgError
from ecg.domains.ecg.models import ECG, Lead
from ecg.domains.ecg.repositories import create, get
from ecg.sql.ecg import CREATE_ECG_QUERY, GET_ECG_BY_ID_QUERY


@pytest.fixture
def ecg_data():
    return ECG(
        id=str(uuid4()),
        owner_id=str(uuid4()),
        date=datetime.now().isoformat(),
        leads=[
            Lead(name="I", signal=[1, 2, 3]),
            Lead(name="II", signal=[2, 3, 4]),
        ],
    )


@pytest.fixture
def db_mock(mocker):
    return mocker.Mock(spec=Database)


@pytest.mark.asyncio
async def test_create(db_mock, ecg_data):
    db_mock.execute.return_value = None

    await create(db_mock, ecg_data)

    db_mock.execute.assert_any_call(
        CREATE_ECG_QUERY,
        {"id": ecg_data.id, "owner_id": ecg_data.owner_id, "date": ecg_data.date},
    )


@pytest.mark.asyncio
async def test_create_ecg_unique_violation(db_mock, ecg_data):
    db_mock.execute.side_effect = UniqueViolationError(None, None, None)

    with pytest.raises(UniqueEcgError):
        await create(db_mock, ecg_data)

    db_mock.execute.assert_called_with(
        CREATE_ECG_QUERY,
        {"id": ecg_data.id, "owner_id": ecg_data.owner_id, "date": ecg_data.date},
    )


@pytest.mark.asyncio
async def test_get(mocker, db_mock, ecg_data):
    mock_get_leads = mocker.patch("ecg.domains.ecg.repositories._get_leads_by_ecg_id")
    db_mock.fetch_one.return_value = ecg_data.dict(exclude={"leads"})
    mock_get_leads.return_value = ecg_data.leads

    result = await get(db_mock, ecg_data.id)

    db_mock.fetch_one.assert_called_once_with(
        GET_ECG_BY_ID_QUERY, {"ecg_id": ecg_data.id}
    )
    mock_get_leads.assert_called_once_with(db_mock, ecg_data.id)

    assert result == ecg_data


@pytest.mark.asyncio
async def test_get_not_found(db_mock, ecg_data):
    db_mock.fetch_one.return_value = None

    result = await get(db_mock, ecg_data.id)

    db_mock.fetch_one.assert_called_once_with(
        GET_ECG_BY_ID_QUERY, {"ecg_id": ecg_data.id}
    )
    assert result is None
