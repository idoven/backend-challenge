from databases import Database

from ecg.config import settings
from ecg.domains.admin import services as admin_services
from ecg.sql.admin import CREATE_USERS_TABLE_SQL


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
    await db.disconnect()
