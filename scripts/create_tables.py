import asyncio
import os
import sys

# make repo root importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# import the app DB pieces
from app.db.session import engine
from app.db.base import Base

async def run():
    async with engine.begin() as conn:
        # create all tables defined on Base.metadata
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(run())
    print("tables created")
