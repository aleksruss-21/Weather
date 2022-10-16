from abc import ABC, abstractmethod
from typing import Dict


class StorageWrapper(ABC):
    """
    Abstract StorageWrapper class that provides access to the storage backend
    """

    @abstractmethod
    async def icao_upload(self, icao_data: dict) -> None:
        pass

    @abstractmethod
    async def timestamps_upload(self, timestamp_data: dict) -> None:
        pass

    @abstractmethod
    async def geo_query(self, icao: dict) -> list[Dict]:
        pass

    @abstractmethod
    async def id_query(self, icao: dict) -> list[Dict]:
        pass
