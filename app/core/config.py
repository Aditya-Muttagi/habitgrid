from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "HabitGrid")
    env: str = os.getenv("ENV", "dev")
    secret_key: str = os.getenv("SECRET_KEY", "default-secret")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

settings = Settings()
