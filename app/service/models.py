from dataclasses import dataclass


@dataclass()
class Id:
    """Schema dataclass for /id requests"""

    icao: str
    start: int
    end: int


@dataclass()
class Geo:
    """Schema dataclass for /geo requests"""

    lat: float
    long: float
    radius: int
    start: int
    end: int
