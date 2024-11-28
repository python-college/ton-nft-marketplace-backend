from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB_NAME: str

    TON_API_KEY: str
    IS_TESTNET: bool

    class Config:
        env_file = ".env"


settings = Settings()
