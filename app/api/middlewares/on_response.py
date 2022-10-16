"""ON-RESPONSE middlewares."""
import time

from sanic import HTTPResponse, Request  # type: ignore
from sanic.log import logger  # type: ignore


async def send_metrics(request: Request, response: HTTPResponse) -> None:
    """Sends metrics and fixes headers for CORS on response."""
    response_time = time.time() - request.ctx.start
    logger.info(f"{request.method} {request.raw_url.decode('utf-8')} : {response_time} ms")
