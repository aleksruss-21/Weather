import requests
import asyncio
import aiohttp  # type: ignore
from aiohttp import ClientConnectorError, ClientOSError

from app.service.get_data.process_data import ProcessStationData, ProcessStationsText  # type: ignore
from app.storage.mongo_client import DB


class CollectData(object):
    def __init__(
        self,
        stations: ProcessStationsText,
        database: DB,
    ) -> None:
        self.stations = stations
        self.database = database

    async def get_stations_txt(self) -> None:
        """Download stations.txt"""
        self.resp: requests.Response = requests.get("https://www.aviationweather.gov/docs/metar/stations.txt")

        with open("stations.txt", "w") as file:
            file.write(self.resp.text)

        await self.stations.process_stations_txt()


class CollectWeatherData(object):
    def __init__(self, station_weather_data: ProcessStationData, db_weather_data: DB) -> None:
        self.station_weather_data = station_weather_data
        self.db_weather_data = db_weather_data

    async def get_station_data(self, icao: str) -> None:
        """Get station data for every icao, make task for process file and upload weather data to database."""
        base_url = "https://tgftp.nws.noaa.gov/data/observations/metar/decoded/"
        try:
            sem = asyncio.Semaphore(1)
            async with sem:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{base_url}{icao}.TXT") as resp:
                        if resp.status == 200:
                            data = await resp.text()
                            station_dict = await self.station_weather_data.process_station_data(
                                station_data=data, icao=icao
                            )
                            await self.db_weather_data.timestamps_upload(station_dict)
        except ValueError:
            pass
        except asyncio.TimeoutError:
            await self.get_station_data(icao)
        except ClientConnectorError:
            await asyncio.sleep(5)
            await self.get_station_data(icao)
        except ClientOSError:
            await self.get_station_data(icao)
        await asyncio.sleep(20)

