import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    def __init__(sef, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        logger.info(f"{request.method} Request to {request.url.path} took {duration:.4f} seconds")
        return response