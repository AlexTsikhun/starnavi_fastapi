import os

from pydantic.v1 import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Starnavi FastAPI API"

    DATABASE_URL: str | None = "sqlite:///./starnavi_fastapi.db"

    secret_key: str = os.getenv("SECRET_KEY", "your_strong_secret")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
