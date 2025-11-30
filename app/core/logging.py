import json, logging, os, uuid, pathlib
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from typing import Callable
from .config import settings

LOG_DIR = pathlib.Path(settings.LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if "file" in settings.LOG_EXPORTERS_JSON:
        handler = RotatingFileHandler(
            LOG_DIR / f"{settings.LOG_FILE_BASENAME}.log",
            maxBytes=settings.LOG_ROTATION_MB * 1024 * 1024,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        formatter = logging.Formatter('{"ts":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if "stdout" in settings.LOG_EXPORTERS_JSON:
        sh = logging.StreamHandler()
        formatter = logging.Formatter('{"ts":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request, call_next: Callable):
        cid = request.headers.get(self.header_name) or str(uuid.uuid4())
        request.state.correlation_id = cid
        response = await call_next(request)
        response.headers[self.header_name] = cid
        return response
