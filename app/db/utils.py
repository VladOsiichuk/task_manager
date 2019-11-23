from app.db.models import db
from app.core.config import DB_URL


async def create_connection():
    await db.set_bind(DB_URL)


async def close_connection():
    await db.pop_bind().close()
