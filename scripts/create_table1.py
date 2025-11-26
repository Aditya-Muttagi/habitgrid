# scripts/create_tables_neon.py
import asyncio
import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine

# --- EDIT these imports if your project differs ---
# The Base used by your SQLAlchemy models
try:
    # common location — adjust if your Base lives elsewhere
    from app.db.base import Base  # <- change this if your Base is in another module
    # ensure your models are imported so Base.metadata is populated
    import app.models.user   # <- import all modules that define models
except Exception:
    # fallback: try alternate location
    from app.db.base import Base
    import app.models.user
# -------------------------------------------------

# Read DATABASE_URL from env if present; otherwise fallback (for local testing)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_OJtU71icGaAg@ep-jolly-truth-a1pr7crh-pooler.ap-southeast-1.aws.neon.tech/neondb"
)

# IMPORTANT: if your original Neon URL had ?sslmode=require or channel_binding, strip them.
# create SSL context for asyncpg
ssl_context = ssl.create_default_context()

# create async engine with proper connect_args for asyncpg + SSL
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context},
)

async def create_all():
    # ensure models are imported (side-effect) so metadata is populated
    # e.g. import app.models.user    # already imported above
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(create_all())
