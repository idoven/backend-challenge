from databases import Database
from ecg.config import settings

# Create a Database instance
database = Database(settings.database_url)


async def get_db():
    if not database.is_connected:
        await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()
