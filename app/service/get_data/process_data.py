import time
import re
import os
import aiohttp  # type: ignore
from datetime import timedelta, datetime as dt
from app.storage.mongo_client import DB
from typing import Dict, Union


class ProcessStationData(object):
    def __init__(self, storage: DB):
        self.storage = storage

    async def process_station_data(self, station_data: str, icao: str) -> Dict[str, Union[str, int, float]]:
        """Process station data into dictionary format"""
        self.station_dict: dict = {
            "icao": icao,
            "date": "",
            "temperature": "",
            "pressure": "",
            "wind_direction": "",
            "wind_speed": "",
        }

        station_data_arr = station_data.split("\n")
        data_collection_time = station_data_arr[1].split("/ ")[1]
        self.station_dict["date"] = int(time.mktime(dt.strptime(data_collection_time, "%Y.%m.%d %H%M UTC").timetuple()))
        for item in station_data_arr:
            if item.startswith("Temperature"):
                temp_data = re.search(r"(\d*\.|)\d* C", item)
                if temp_data is not None:
                    self.station_dict["temperature"] = temp_data.group().split()[0]
            elif item.startswith("Pressure"):
                pressure_data = re.search(r"(-|)\d* hPa", item)
                if pressure_data is not None:
                    self.station_dict["pressure"] = pressure_data.group().split()[0]
            elif item.startswith("Wind:"):
                if "Calm" in item:
                    self.station_dict["wind_speed"] = "0"
                else:
                    wind_direction_data = re.search(r"\d* degrees", item)
                    wind_speed_data = re.search(r"\d* KT", item)
                    if wind_direction_data is not None:
                        self.station_dict["wind_direction"] = wind_direction_data.group().split()[0].lstrip("0")
                    if wind_speed_data is not None:
                        self.station_dict["wind_speed"] = wind_speed_data.group().split()[0]
        return self.station_dict


class ProcessStationsText(object):
    def __init__(self, storage: DB):
        self.storage = storage
        self.icao: dict = {}

    async def process_stations_txt(self) -> None:
        """Get stations.txt from the server and process file"""

        with open("stations.txt", "r") as base:
            index = 0
            for line in base:
                if not line.startswith("!") and " " not in line[39:41] and "STATION" not in line and line[39:41] != "":
                    icao_index = line[20:24]
                    lat_index = round(int(line[39:41]) + int(line[42:44]) / 60, 6)
                    long_index = round(int(line[47:50]) + int(line[51:53]) / 60, 6)

                    self.icao[index] = {
                        "icao": icao_index,
                        "location": {
                            "type": "Point",
                            "coordinates": [long_index, lat_index],
                        },
                    }
                    await self.storage.icao_upload(icao_data=self.icao[index])
                    index += 1

        os.remove("stations.txt")


async def get_stations_to_parse() -> list[str]:
    """Get stations array with new reports in last 30 minutes"""
    url = "https://tgftp.nws.noaa.gov/data/observations/metar/decoded/?C=M;O=D"
    async with aiohttp.request("GET", url) as response:
        text = await response.text()
        with open("list.txt", "w") as file:
            file.write(text)

        with open("list.txt", "r") as file:
            arr = []
            for line in file:
                if re.match('^<tr><td><a href=".....TXT*', line):
                    icao = line[17:21]
                    date_report = line[62:79]
                    datetime_format = dt.strptime(date_report, "%d-%b-%Y %H:%M")
                    if dt.utcnow() - datetime_format < timedelta(minutes=30):
                        arr.append(icao)
    os.remove("list.txt")
    return arr
