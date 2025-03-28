from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Настройки проекта, загружаемые из переменных окружения.
    """
    api_id: int = Field(..., env="API_ID")
    api_hash: str = Field(..., env="API_HASH")
    phone_number: str = Field(..., env="PHONE_NUMBER")
    session_file_path: str = Field(default="anon", env="SESSION_FILE_PATH")
    telegram_channels: List[int] = Field(default_factory=[], env="TELEGRAM_CHANNELS")

    postgres_user: str = Field(default='tg_scrap', env="POSTGRES_USER")
    postgres_password: str = Field(default='tg_scrap', env="POSTGRES_PASSWORD")
    db_name: str = Field(default='tg_scrap', env="DB_NAME")
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_engine: str = Field(default="postgresql+asyncpg", env="DB_ENGINE")

    @property
    def DATABASE_URL(self) -> str:

        return (f'{self.db_engine}://{self.postgres_user}:{self.postgres_password}@{self.db_host}:'
                f'{self.db_port}/{self.db_name}')

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()
