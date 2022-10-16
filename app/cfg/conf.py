"""Global configuration."""

import asyncio
import logging
import os
import sys

import uvloop  # type: ignore

__all__ = ["get_config", "Config"]
__version__ = os.getenv("API_VERSION", "1.0.0")

log_level = os.getenv("LOGLEVEL", "DEBUG")
logging.basicConfig(format="%(name)s %(levelname)-4s [%(asctime)s] %(message)s", level=log_level)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
TEST_MODE = bool(int(os.getenv("TEST_MODE", 0)))


class Config:
    """Global config object."""

    def __init__(self) -> None:
        self.VERSION: str = __version__
        self.version: str = __version__.split(".")[0]
        self.loglevel: str = log_level
        self.mongo = self._MongoMeta()
        self.redis = self.Cache()
        self.logging_config = dict(
            version=1,
            disable_existing_loggers=False,
            loggers={
                "sanic.root": {"level": f"{log_level}", "handlers": ["console"]},
                "sanic.error": {
                    "level": f"{log_level}",
                    "handlers": ["error_console"],
                    "propagate": True,
                    "qualname": "sanic.error",
                },
                "sanic.access": {
                    "level": f"{log_level}",
                    "handlers": ["access_console"],
                    "propagate": True,
                    "qualname": "sanic.access",
                },
            },
            handlers={
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "generic",
                    "stream": sys.stdout,
                },
                "error_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "generic",
                    "stream": sys.stderr,
                },
                "access_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "access",
                    "stream": sys.stdout,
                },
            },
            formatters={
                "generic": {
                    "format": "[%(name)s %(levelname)-4s %(asctime)s]: " + "%(message)s",
                    "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                    "class": "logging.Formatter",
                },
                "access": {
                    "format": "[%(name)s %(levelname)s %(asctime)s] - %(host)s: "
                    + "%(request)s %(message)s %(status)d (%(byte)d bytes)",
                    "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                    "class": "logging.Formatter",
                },
            },
        )

    class APIConfig:
        """Sanic configuration."""

        DEBUG = True if log_level == "DEBUG" else False
        ACCESS_LOG = bool(int(os.getenv("ACCESS_LOG", 1)))
        REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))
        RESPONSE_TIMEOUT = int(os.getenv("RESPONSE_TIMEOUT", 5))
        KEEP_ALIVE_TIMEOUT = int(os.getenv("KEEP_ALIVE_TIMEOUT", 60))
        FORWARDED_SECRET = os.getenv("FORWARDED_SECRET")
        REAL_IP_HEADER = os.getenv("REAL_IP_HEADER")
        PROXIES_COUNT = os.getenv("PROXIES_COUNT")
        GRACEFUL_SHUTDOWN_TIMEOUT = 1
        FALLBACK_ERROR_FORMAT = "json"

    class _MongoMeta:
        """Mongo connection configuration."""

        def __init__(self) -> None:
            self._host = os.getenv("MONGO_HOST", "mongo")
            self._port = int(os.getenv("MONGO_PORT", 27017))
            self.db: str = os.getenv("MONGO_DATABASE", "icao")
            self.collection_icao = os.getenv("COLLECTION", "icao")
            self.collection_weather_data = os.getenv("COLLECTION", "weather_data")

            uri = f"mongodb://{self._host}:{self._port}/{self.db}"

            self.uri = os.getenv("MONGO_URI", uri)

    class Cache:
        """Redis connection configuration."""

        def __init__(self) -> None:
            self.host = os.getenv("REDIS_HOST", "redis")
            self.port = os.getenv("REDIS_PORT", 6379)


def get_config() -> Config:
    """Get Config instance."""
    return Config()
