from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "DMBAI"
    OPENAI_API_KEY: str
    ANTROPIC_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()