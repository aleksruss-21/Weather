"""Abstract interfaces module."""
from typing import Any, Iterable, Optional, Union

from sanic import HTTPResponse, Request, json  # type: ignore
from sanic.log import logger  # type: ignore
from sanic.response import empty  # type: ignore
from sanic.views import HTTPMethodView  # type: ignore
from sanic_ext import openapi  # type: ignore


class BaseView(HTTPMethodView):
    """Base class-based view providing all HTTP-methods."""

    @classmethod
    async def ok_response(cls, request: Request, response: Union[str, int, float, Iterable, dict]) -> HTTPResponse:
        """Return OK and message."""
        code = 200
        if request.method == "POST":
            code = 201
        if isinstance(response, str):
            return json({"code": code, "message": response}, status=code)
        return json(response, code)

    @classmethod
    async def bad_request(cls, request: Request, exception: Optional[str] = None) -> HTTPResponse:
        """Return 400 "Bad Request" and message."""
        if exception:
            logger.exception(f"Code 400: {exception}")
            return json({"code": 400, "message": f"Bad request: {exception}"}, status=400)
        return json({"code": 400, "message": "Bad request"}, status=400)

    @classmethod
    async def not_found(cls, request: Request, exception: Optional[str] = None) -> HTTPResponse:
        """Return 404 "Not Found" and message."""
        if exception:
            logger.exception(f"Code 404: {exception}")
            return json({"code": 404, "message": f"Not found: {exception}"}, status=404)
        return json({"code": 404, "message": "Not found"}, status=404)

    @classmethod
    async def method_not_allowed(cls, request: Request) -> HTTPResponse:
        """Return 405 "Method Not Allowed" and message."""
        return json(
            {
                "code": 405,
                "message": f"Method not allowed: {request.method} {request.url}",
            },
            status=405,
        )

    @classmethod
    async def server_error(cls, request: Request, exception: Exception) -> HTTPResponse:
        """Return 500 "Internal Server Error" and message."""
        logger.exception(f"Code 500: {exception}")
        message = exception.args[0]
        return json({"code": 500, "exception": message}, status=500)

    @openapi.exclude(True)
    async def get(self, request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return await self.method_not_allowed(request)

    @openapi.exclude(True)
    async def post(self, request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return await self.method_not_allowed(request)

    @openapi.exclude(True)
    async def put(self, request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return await self.method_not_allowed(request)

    @openapi.exclude(True)
    async def patch(self, request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return await self.method_not_allowed(request)

    @openapi.exclude(True)
    async def delete(self, request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return await self.method_not_allowed(request)

    @staticmethod
    async def head(request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return empty()

    @staticmethod
    async def options(request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
        return empty()
