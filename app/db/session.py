from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./habitgrid.db")

engine = create_async_engine(DATABASE_URL, echo=False)

# Every API request that accesses the database must use its own session.
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    db= AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
