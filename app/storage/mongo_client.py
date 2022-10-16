from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase  # type: ignore
import asyncio
from abc import ABC

from app.service.storage import StorageWrapper
from typing import Dict
from app.cfg import config


class MongoClient:
    """An object for establishing connection with a database on a mongodb-server."""

    def __init__(self, uri: str, db: str):
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
        self._client.get_io_loop = asyncio.get_event_loop
        self.db: AsyncIOMotorDatabase = self._client[db]

    def __del__(self) -> None:
        self._client.close()


class DB(StorageWrapper, ABC):
    """Database management client connected to a certain collection within one database.

    Awaits a {db}-attribute of a MongoClient-instance and a collection name.
    """

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str) -> None:
        self.collection = db[collection_name]

    async def icao_upload(self, icao_data: dict) -> None:
        """Upload icao data to database, if it is not in database"""
        is_exist = await self.collection.count_documents({"icao": icao_data["icao"]}) != 0
        if not is_exist:
            await self.collection.insert_one(icao_data)

    async def timestamps_upload(self, timestamp_data: dict) -> None:
        """Upload weather data to database"""
        icao_name = timestamp_data["icao"]
        date = timestamp_data["date"]
        is_exist = await self.collection.count_documents({"$and": [{"icao": icao_name}, {"date": date}]}) != 0
        if not is_exist:
            await self.collection.insert_one(timestamp_data)

    async def id_query(self, icao: dict) -> list[Dict]:
        icao_name = str(*icao["icao"])
        start = int(*icao["start"])
        end = int(*icao["end"])

        cursor = self.collection.find({"$and": [{"icao": icao_name}, {"date": {"$gte": start, "$lte": end}}]})

        report_to_return = []
        async for doc in cursor:
            report = {
                "icao": doc["icao"],
                "date": doc["date"],
                "temperature": doc["temperature"],
                "pressure": doc["pressure"],
                "wind_direction": doc["wind_direction"],
                "wind_speed": doc["wind_speed"],
            }
            report_to_return.append(report)
        return report_to_return

    @staticmethod
    async def geo_radius_filter(longitude: float, latitude: float, radius: int) -> list[dict]:
        """Get the list of ICAO in request radius"""
        collection_icao = get_db(config.mongo.collection_icao).collection
        radius_query = {
            "location": {
                "$near": {"$geometry": {"type": "Point", "coordinates": [longitude, latitude]}, "$maxDistance": radius}
            },
        }
        return [doc["icao"] async for doc in collection_icao.find(radius_query)]

    async def geo_query(self, icao: dict) -> list[Dict]:
        """Filter by date and radius and find weather data at DB"""
        lat = float(*icao["lat"])
        lon = float(*icao["lon"])
        radius = int(*icao["radius"])
        start = int(*icao["start"])
        end = int(*icao["end"])

        radius_filtered = await self.geo_radius_filter(lon, lat, radius)

        time_filtered = self.collection.find(
            {"$and": [{"icao": {"$in": radius_filtered}}, {"date": {"$gte": start, "$lte": end}}]}
        )

        report_to_return = []
        async for doc in time_filtered:
            report = {
                "icao": doc["icao"],
                "date": doc["date"],
                "temperature": doc["temperature"],
                "pressure": doc["pressure"],
                "wind_direction": doc["wind_direction"],
                "wind_speed": doc["wind_speed"],
            }
            report_to_return.append(report)
        return report_to_return


def get_mongo_client() -> MongoClient:
    """Get MongoClient instance."""
    return MongoClient(uri=config.mongo.uri, db=config.mongo.db)


def get_db(collection: str, db_client: MongoClient = None) -> DB:
    """Get DB client"""
    if not db_client:
        db_client = get_mongo_client()
    return DB(db=db_client.db, collection_name=collection)
