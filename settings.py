from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Starnavi FastAPI API"

    DATABASE_URL: str | None = "sqlite:///./starnavi_fastapi.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
