from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"
    database_url: str

    mail_username: str
    mail_password: str
    mail_server: str
    mail_port: int

    celery_broker_url: str
    celery_result_backend: str

    redis_host: str = "localhost"
    redis_port: int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()