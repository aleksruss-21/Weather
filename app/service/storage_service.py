from app.service.storage import StorageWrapper
from app.service.cache import CacheMiss, CacheWrapper
from typing import Dict, Union


class StorageService(object):
    def __init__(self, storage: StorageWrapper, cache: CacheWrapper) -> None:
        self.storage = storage
        self.cache = cache

    async def icao_upload(self, icao_data: dict) -> None:
        """Call storage db method icao_upload"""
        return await self.storage.icao_upload(icao_data=icao_data)

    async def timestamps_upload(self, timestamp_data: Dict[str, Union[str, int, float]]) -> None:
        """Call storage db method timestamps_upload"""
        return await self.storage.timestamps_upload(timestamp_data)

    async def geo_query(self, icao: dict) -> list[Dict]:
        """Check if geo query exists in cache else call database"""
        try:
            geo_report = await self.cache.get_geo_query(icao.copy())
            return geo_report
        except CacheMiss:
            geo_report = await self.storage.geo_query(icao)
            if len(geo_report) != 0:
                await self.cache.set_geo_query(icao, geo_report)
            return geo_report

    async def id_query(self, icao: dict) -> list[Dict]:
        """Check if id query exists in cache else call database"""
        try:
            id_report = await self.cache.get_id_query(icao.copy())
            return id_report
        except CacheMiss:
            id_report = await self.storage.id_query(icao)
            if len(id_report) != 0:
                await self.cache.set_id_query(icao, id_report)
            return id_report
