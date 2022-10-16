"""API blueprints."""
from sanic import Blueprint  # type: ignore

from app.cfg import config

__all__ = ["api_blueprints", "id_bp", "geo_bp"]

id_bp = Blueprint("base", version=config.version)
geo_bp = Blueprint("geo", version=config.version)

api_blueprints = Blueprint.group(id_bp, geo_bp)
