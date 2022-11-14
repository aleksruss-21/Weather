from .celery import app
from app.storage.mongo_client import get_db
from app.service.get_data.process_data import ProcessStationData, ProcessStationsText, get_stations_to_parse
from app.service.get_data.collect import CollectWeatherData, CollectData
import asyncio
import os


async def upload_icao():
    """To request stations.txt, process and add to database"""
    db_icao = get_db(collection=os.getenv("MONGO_DATABASE", "icao"))
    process = ProcessStationsText(db_icao)
    collect_data = CollectData(process, db_icao)
    await collect_data.get_stations_txt()


@app.task
def get_icao() -> None:
    """Wrapper to launch async function"""
    asyncio.run(upload_icao())


async def upload_weather_data() -> None:
    """To request weather data, process and upload to database"""
    db_weather_data = get_db(collection=os.getenv("MONGO_DATABASE", "weather_data"))
    station = ProcessStationData(storage=db_weather_data)
    collect_weather_data = CollectWeatherData(station, db_weather_data)
    await asyncio.gather(*(collect_weather_data.get_station_data(item) for item in await get_stations_to_parse()))


@app.task
def get_weather_data() -> None:
    """Wrapper to launch async function"""
    asyncio.run(upload_weather_data())
