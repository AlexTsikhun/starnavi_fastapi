from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Starnavi FastAPI API"
    DATABASE_URL: str = "sqlite:///./starnavi_fastapi.db"
    GEMINI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = "30"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
