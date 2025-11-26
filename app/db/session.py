from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:aditya1729@localhost/HabitGridDatabase")

engine = create_async_engine(DATABASE_URL, echo=False,future=True)

# Every API request that accesses the database must use its own session.
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
    future=True,
)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
