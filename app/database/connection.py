import asyncpg
from app.config.settings import settings


async def get_asyncpg_connection():
    """Get direct asyncpg connection for raw SQL queries"""
    # Convert SQLAlchemy URL to asyncpg format
    db_url = settings.get_database_url.replace("postgresql://", "")
    return await asyncpg.connect(db_url)