"""ON-REQUEST middlewares."""
import time
from sanic import Request  # type: ignore
from sanic.response import HTTPResponse, empty  # type: ignore
from typing import Optional

from app.api.routes.base_view import BaseView  # type: ignore


async def validate_request(request: Request) -> HTTPResponse | None:
    """Validates request path, query and body parameters of request"""
    request.ctx.start = time.time()

    if not request.route:
        return empty()
    elif request.route.path == "id":
        found_error_id: Optional[str] = await validate_id_request(request)
        if found_error_id:
            return await BaseView.bad_request(request, found_error_id)
    elif request.route.path == "geo":
        found_error_geo: Optional[str] = await validate_geo_request(request)
        if found_error_geo:
            return await BaseView.bad_request(request, found_error_geo)


async def validate_id_request(request: Request) -> str | None:
    """Validates request path, query and body parameters of /id request"""
    if request.args.get("icao") is None:
        return "'icao' parameter is required"
    date_error = await validate_date(request)
    if date_error:
        return date_error


async def validate_geo_request(request: Request) -> str | None:
    """Validates request path, query and body parameters of /geo request"""
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = request.args.get("radius")
    if lat is None:
        return "'lat' parameter is required"
    if lon is None:
        return "'lon' parameter is required"
    if radius is None:
        return "'radius' parameter is required"

    try:
        int(radius)
    except ValueError:
        return "'radius' parameter must be int type"

    if int(radius) < 0:
        return "'radius' parameter must be greater than 0"

    try:
        float(lat)
        float(lon)
    except ValueError:
        return "'lat' and 'lon' parameters must be int or float types"

    if float(lon) >= 180 or float(lon) <= -180:
        return "longitude must be between -180 and 180, inclusive."
    if float(lat) <= -90 or float(lat) >= 90:
        return "latitude must be between -90 and 90, inclusive."


async def validate_date(request: Request) -> str | None:
    """Validate Date parameters"""
    start = request.args.get("start")
    end = request.args.get("end")
    if start is None:
        return "'start' parameter is required"
    if end is None:
        return "'end' parameter is required"

    try:
        start = int(start)
        end = int(end)
    except ValueError:
        return "date parameters must be int type"

    if int(start) < 0 or int(end) < 0:
        return "date parameters must be greater than 0"
