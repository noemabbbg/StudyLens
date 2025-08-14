from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    tg_token: str | None = None
    mongo_uri: str = "mongodb://mongo:27017"
    s3_endpoint: str | None = None
    s3_key: str | None = None
    s3_secret: str | None = None
    llm_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
