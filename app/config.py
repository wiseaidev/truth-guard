"""Configurations module."""

from functools import (
    lru_cache,
)
import os
from pydantic import (
    BaseSettings,
)
from typing import (
    List,
)


class Settings(BaseSettings):
    """
    A Pydantic class that loads and stores environment variables in memory.

    Note:
        The os.getenv is used in production.

    Args:
        DEBUG (str) : A variable used to separate testing env from production env.
        CORS_ORIGINS (str) : A string that contains comma separated urls for cors origins.

    Example:
        >>> DEBUG="" # "" means production, "test" means testing, "info" means development.
        >>> CORS_ORIGINS="https://app-name.herokuapp.com,http://app-name.pages.dev"
    """

    DEBUG: str = os.getenv("DEBUG")  # type: ignore
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")  # type: ignore

    class Config:  # pylint: disable=R0903
        """
        A class used to set Pydantic configuration for env vars.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins(self) -> List[str]:
        """
        Build a list of urls from a comma separated values string.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            List[str]: A list of urls.
        """
        return (
            [url.strip() for url in self.CORS_ORIGINS.split(",") if url]
            if self.CORS_ORIGINS
            else []
        )


@lru_cache()
def settings() -> Settings:
    """
    Return a cached Settings instance.

    Returns:
        Settings: The app settings.
    """
    return Settings()


# Export module

__all__ = ["settings"]
