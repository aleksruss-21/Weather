"""ON-START listeners."""
from asyncio import AbstractEventLoop

from sanic import Sanic  # type: ignore

from app.cache.cache import get_cache_instance
from app.service.storage_service import StorageService
from app.storage.mongo_client import get_db


async def create_app_context(app: Sanic, loop: AbstractEventLoop) -> None:
    """A "BEFORE_SERVER_START" listener.

    On the application start creates database client, service and puts them into application context.
    """
    storage_icao = get_db(app.ctx.config.mongo.collection_icao)
    storage_weather_data = get_db(app.ctx.config.mongo.collection_weather_data)
    cache = get_cache_instance()
    storage_service_icao = StorageService(storage=storage_icao, cache=cache)
    storage_service_weather_data = StorageService(storage=storage_weather_data, cache=cache)
    app.ext.dependency(storage_service_icao)
    app.ext.dependency(storage_service_weather_data)
