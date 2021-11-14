from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    ENCODER_SECRET_KEY: str
    ENCODER_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = ".env"


config = Settings()
