"""ID requests."""
# import dataclasses

from sanic import HTTPResponse, Request, json  # type: ignore
from sanic_ext import openapi  # type: ignore

from app.api.routes.base_view import BaseView
from app.api.schemas import IdSchema, GeoSchema, Schema20x40x, Schema5xx
from app.service.storage_service import StorageService


class IDEvents(BaseView):
    """View of operations on ID events."""

    @openapi.response(200, [IdSchema], description="OK")
    @openapi.response(400, Schema20x40x, description="Bad Request")
    @openapi.response(404, Schema20x40x, description="Not Found")
    @openapi.response(500, Schema5xx, description="Internal Server Error")
    @openapi.parameter(
        name="end", description="end unix timestamp", location="query", required=True, allowEmptyValue=False, schema=int
    )
    @openapi.parameter(
        name="start",
        description="start unix timestamp",
        location="query",
        required=True,
        allowEmptyValue=False,
        schema=int,
    )
    @openapi.parameter(
        name="icao", description="ICAO title", location="query", required=True, allowEmptyValue=False, schema=str
    )
    async def get(self, request: Request, storage: StorageService) -> HTTPResponse:
        """Get all events for a given trigger ID."""
        icao = request.args.get("icao")
        start = request.args.get("start")
        end = request.args.get("end")
        if icao is None:
            return await self.bad_request(request, "icao is required")
        if start is None:
            return await self.bad_request(request, "start time is required")
        if end is None:
            return await self.bad_request(request, "end time is required")
        icao_data = await storage.id_query(request.args)
        return json(icao_data)


class GeoEvents(BaseView):
    """View of operations on Geo Events."""

    @openapi.response(200, [GeoSchema], description="OK")
    @openapi.response(400, Schema20x40x, description="Bad Request")
    @openapi.response(404, Schema20x40x, description="Not Found")
    @openapi.response(500, Schema5xx, description="Internal Server Error")
    @openapi.parameter(
        name="radius",
        description="radius, in meters",
        location="query",
        required=True,
        allowEmptyValue=False,
        schema=int,
    )
    @openapi.parameter(
        name="end", description="end unix timestamp", location="query", required=True, allowEmptyValue=False, schema=int
    )
    @openapi.parameter(
        name="start",
        description="start unix timestamp",
        location="query",
        required=True,
        allowEmptyValue=False,
        schema=int,
    )
    @openapi.parameter(
        name="lon",
        description="longitude, decimal format",
        location="query",
        required=True,
        allowEmptyValue=False,
        schema=float,
    )
    @openapi.parameter(
        name="lat",
        description="latitude, decimal format",
        location="query",
        required=True,
        allowEmptyValue=False,
        schema=float,
    )
    async def get(self, request: Request, storage: StorageService) -> HTTPResponse:
        """Get all events for a given trigger ID."""
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        radius = request.args.get("radius")
        start = request.args.get("start")
        end = request.args.get("end")
        if lat is None:
            return await self.bad_request(request, "latitude is required")
        if lon is None:
            return await self.bad_request(request, "longitude is required")
        if radius is None:
            return await self.bad_request(request, "radius is required")
        if start is None:
            return await self.bad_request(request, "start time is required")
        if end is None:
            return await self.bad_request(request, "end time is required")

        icao_data = await storage.geo_query(request.args)
        return json(icao_data)
