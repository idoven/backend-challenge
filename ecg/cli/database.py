from datetime import datetime

from databases import Database

from ecg.config import settings
from ecg.domains.admin import services as admin_services
from ecg.domains.admin.exceptions import NotUniqueUserError
from ecg.domains.ecg import services as ecg_services
from ecg.domains.ecg.exceptions import UniqueEcgError
from ecg.domains.ecg.models import ECG, Lead
from ecg.sql.admin import CREATE_USERS_TABLE_SQL
from ecg.sql.ecg import CREATE_ECG_TABLE_SQL, CREATE_LEAD_TABLE_SQL


async def create_user_table():
    db = Database(settings.database_url)
    await db.connect()
    await db.execute(CREATE_USERS_TABLE_SQL)
    await db.disconnect()
    print("Users table created successfully!")


async def populate_user_table():
    db = Database(settings.database_url)
    admin = admin_services.generate_user(
        email="admin@test.com",
        password="admin",
        admin=True,
    )
    await db.connect()
    try:
        await admin_services.create_user(
            db,
            creator=admin,
            email=admin.email,
            password="admin",
            admin=True,
        )
        await admin_services.create_user(
            db,
            creator=admin,
            email="test@test.com",
            password="test",
            admin=False,
        )
    except NotUniqueUserError:
        print("Users already created!")
    finally:
        await db.disconnect()


async def create_ecgs_tables():
    db = Database(settings.database_url)
    await db.connect()
    await db.execute(CREATE_ECG_TABLE_SQL)
    await db.execute(CREATE_LEAD_TABLE_SQL)
    await db.disconnect()
    print("ECGs table created successfully!")


async def populate_ecgs_tables():
    db = Database(settings.database_url)
    await db.connect()
    user = await admin_services.get_user(db, "test@test.com")
    ecg = ECG(
        id="testid",
        owner_id=user.id,
        date=datetime.now(),
        leads=[
            Lead(
                name="I",
                signal=[1, 2, 3, 4, 5, -6, -7, -8, 9, 10],
            )
        ],
    )
    try:
        await ecg_services.create(db, user, ecg)
    except UniqueEcgError:
        print("ECG already created!")

    await db.disconnect()
    print("ECGs populated successfully!")
