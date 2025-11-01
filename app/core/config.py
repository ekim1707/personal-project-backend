from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    DATABASE_URL: str = "postgresql://admin:admin@localhost:5432/db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
