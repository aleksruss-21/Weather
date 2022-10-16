from abc import ABC, abstractmethod
from typing import Dict


class CacheMiss(Exception):
    """Exception raised when a cache miss is detected"""

    pass


class CacheWrapper(ABC):  # Repository
    """Abstract EventsCacheWrapper class that provides access to the cache"""

    @abstractmethod
    async def get_geo_query(self, icao: dict) -> list[Dict]:
        pass

    @abstractmethod
    async def get_id_query(self, user_id: dict) -> list[Dict]:
        pass

    @abstractmethod
    async def set_geo_query(self, icao: dict, report: list[Dict]) -> None:
        pass

    @abstractmethod
    async def set_id_query(self, icao: dict, report: list[Dict]) -> None:
        pass
