"""API schemas module."""
from dataclasses import dataclass

from app.service.storage_service import StorageService


@dataclass()
class Schema20x40x:
    """Schema of 20x and 40x responses."""

    code: int
    message: str


@dataclass()
class Schema5xx:
    """Schema of 5xx responses."""

    code: int
    exception: str
    request: str


@dataclass()
class IdSchema(StorageService):
    pass


@dataclass()
class GeoSchema(StorageService):
    pass
