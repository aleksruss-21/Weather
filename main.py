"""API application."""
from sanic import Sanic  # type: ignore
from sanic.exceptions import InvalidUsage, MethodNotSupported, NotFound, ServerError  # type: ignore
from sanic_ext import Extend  # type: ignore

from app.api.routes.events import IDEvents, GeoEvents
from app.api.blueprints import api_blueprints
from app.api.middlewares.on_request import validate_request
from app.api.middlewares.on_response import send_metrics
from app.api.middlewares.on_start import create_app_context
from app.api.routes.base_view import BaseView
from app.api.routes.index import IndexRoute
from app.cfg import config


def create_app(*, api_config: object = config.APIConfig, log_config: dict = config.logging_config) -> Sanic:
    """Create and return Sanic application."""
    app = Sanic(name="GetWeather", log_config=log_config)
    app.update_config(api_config)
    app.config["API_VERSION"] = config.VERSION
    app.config["API_TITLE"] = "WeatherData API"
    app.config["API_DESCRIPTION"] = "WeatherData API"
    app.config["API_LICENSE_NAME"] = "Aleksandr"
    app.config["API_CONTACT_EMAIL"] = "be.aleksandrov@gmail.com"

    Extend(app)

    app.listener(create_app_context, "before_server_start")
    app.middleware(validate_request, "request")
    app.middleware(send_metrics, "response")

    app.blueprint(api_blueprints)
    app.add_route(IndexRoute.as_view(), "/", name="index")
    app.add_route(IDEvents.as_view(), "/id", name="id")
    app.add_route(GeoEvents.as_view(), "/geo", name="geo")

    app.error_handler.add(NotFound, BaseView.not_found)
    app.error_handler.add(InvalidUsage, BaseView.bad_request)
    app.error_handler.add(ServerError, BaseView.server_error)
    app.error_handler.add(MethodNotSupported, BaseView.method_not_allowed)
    app.error_handler.add(Exception, BaseView.server_error)

    app.ctx.config = config
    return app


if __name__ == "__main__":
    api = create_app()
    api.run(host="0.0.0.0")
