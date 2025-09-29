from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_PROJECT_ID: str
    SUPABASE_JWKS_URL: str
    SUPABASE_ANON_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()