import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("profile-matcher")

class Settings(BaseModel):
    database_url: str = "sqlite+pysqlite:///./profile_matcher.db"

settings = Settings()
