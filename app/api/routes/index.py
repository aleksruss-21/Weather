"""Base index route module."""

from sanic import HTTPResponse, Request  # type: ignore
from sanic.response import redirect  # type: ignore
from sanic_ext import openapi  # type: ignore

from app.api.routes.base_view import BaseView


class IndexRoute(BaseView):
    """
    Base index route.
    """

    @openapi.tag("Index route")
    @openapi.response(302, None, description="Opens the page where you're now.")
    async def get(self, request: Request) -> HTTPResponse:
        """Redirects to API swagger documentation."""
        return redirect(request.app.url_for("openapi.swagger"))
