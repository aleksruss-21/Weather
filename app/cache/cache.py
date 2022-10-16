from abc import ABC

from app.service.cache import CacheWrapper, CacheMiss

from redis import asyncio as aioredis
from app.cfg import config

from typing import Dict
import json


class EventsCache(CacheWrapper, ABC):
    def __init__(self) -> None:
        self.redis_client: aioredis.Redis = aioredis.Redis(host=config.redis.host, port=int(config.redis.port), db=0)

    async def get_geo_query(self, icao: dict) -> list[Dict]:
        """Check if geo query exist in cache"""
        icao["lat"] = round(float(*icao["lat"]), 2)
        icao["lon"] = round(float(*icao["lon"]), 2)
        icao_encode = json.dumps(icao).encode("utf-8")
        cache = await self.redis_client.get(icao_encode)
        if cache:
            cache_decoded = json.loads(cache)
            return cache_decoded
        else:
            raise CacheMiss

    async def get_id_query(self, icao: dict) -> list[Dict]:
        """Check if id query exist in cache"""
        icao_encode = json.dumps(icao).encode("utf-8")
        cache = await self.redis_client.get(icao_encode)
        if cache:
            cache_decoded = json.loads(cache)
            return cache_decoded
        else:
            raise CacheMiss

    async def set_geo_query(self, icao: dict, report: list[Dict]) -> None:
        """Save geo query in cache"""
        icao["lat"] = round(float(*icao["lat"]), 2)
        icao["lon"] = round(float(*icao["lon"]), 2)
        icao_encode = json.dumps(icao).encode("utf-8")
        report_encode = json.dumps(report).encode("utf-8")
        await self.redis_client.set(icao_encode, report_encode, ex=1700)

    async def set_id_query(self, icao: dict, report: list[Dict]) -> None:
        """Save id query in cache"""
        icao_encode = json.dumps(icao).encode("utf-8")
        report_encode = json.dumps(report).encode("utf-8")
        await self.redis_client.set(icao_encode, report_encode, ex=1700)


def get_cache_instance() -> EventsCache:
    """Call cache class"""
    return EventsCache()
