from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    """
    Application settings loaded from .env
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', validate_assignment=True)

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the database URL from environment variables.
        """
        return "sqlite:///database.db"

    TESTING: bool = False


@lru_cache()
def get_settings():
    return __Settings()


settings = get_settings()
