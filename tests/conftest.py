import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from databases import Database

from ecg.api.dependencies.database import get_db
from ecg.domains.admin.models import User, RoleEnum
from ecg.domains.admin import repositories as admin_repo
from ecg.domains.ecg.models import ECG, LeadTypeEnum
from ecg.domains.ecg import repositories as ecg_repo
from main import app
from ecg.sql.admin import CREATE_USERS_TABLE_SQL
from ecg.sql.ecg import CREATE_ECG_TABLE_SQL, CREATE_LEAD_TABLE_SQL

sys.path.insert(0, str(Path(__file__).parent))

logging.getLogger("databases").setLevel(logging.WARNING)

pytest_user = {
    "id": UUID("19af9e62-4e7f-411c-b50f-791ac56f5ae9"),
    "email": "pytest@test.com",
    "password": "",
    "role": RoleEnum.USER,
}

pytest_admin = {
    "id": UUID("e4152102-367a-4b78-83b7-9fc809d5e169"),
    "email": "admin@test.com",
    "password": "",
    "role": RoleEnum.ADMIN,
}

pytest_ecg = {
    "id": "test_id",
    "name": "test_ecg",
    "date": datetime(2021, 1, 1, 0, 0, 0),
    "owner_id": pytest_user["id"],
    "leads": [
        {
            "signal": [1, 1, -1, -1],
            "name": LeadTypeEnum.I,
        },
        {
            "signal": [-1, 1, -1, -1],
            "name": LeadTypeEnum.II,
        },
    ],
}


@pytest.fixture(scope="session")
def test_user():
    return User(**pytest_user)


@pytest.fixture(scope="session")
def test_admin():
    return User(**pytest_admin)


@pytest.fixture(scope="session")
def test_ecg():
    return ECG(**pytest_ecg)


async def setup_database():
    default_database = Database("postgresql://user:password@db:5432/postgres")

    await default_database.connect()
    await default_database.execute("DROP DATABASE IF EXISTS pytest")
    await default_database.execute("CREATE DATABASE pytest")
    await default_database.disconnect()

    test_database = Database("postgresql://user:password@db:5432/pytest")
    await test_database.connect()
    await test_database.execute(CREATE_USERS_TABLE_SQL)
    await test_database.execute(CREATE_ECG_TABLE_SQL)
    await test_database.execute(CREATE_LEAD_TABLE_SQL)
    await test_database.disconnect()


async def teardown_database():
    default_database = Database("postgresql://user:password@db:5432/postgres")

    await default_database.connect()
    await default_database.execute("DROP DATABASE pytest")
    await default_database.disconnect()


async def populate_tables(db: Database):
    if not db.is_connected:
        await db.connect()
    await admin_repo.create(db, User(**pytest_user))
    await admin_repo.create(db, User(**pytest_admin))
    await ecg_repo.create(db, ECG(**pytest_ecg))


async def clean_tables(db: Database):
    if not db.is_connected:
        await db.connect()
    await db.execute("DELETE FROM users")
    await db.execute("DELETE FROM ecgs")
    await db.execute("DELETE FROM leads")


@pytest.fixture(scope="session")
def setup_teardown_database():
    asyncio.run(setup_database())
    yield
    asyncio.run(teardown_database())


@pytest.fixture(scope="session")
def test_client(setup_teardown_database):
    async def _override_get_db():
        db = Database("postgresql://user:password@db:5432/pytest")
        if not db.is_connected:
            await db.connect()
        try:
            await populate_tables(db)
            yield db
        finally:
            await clean_tables(db)
            await db.disconnect()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
