from fastapi import FastAPI, Request
import uuid

from ..logger import setup_logging, correlation_id
from .routes import packs

setup_logging()
app = FastAPI(title="StudyLens API")
app.include_router(packs.router)


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    corr_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    correlation_id.set(corr_id)
    response = await call_next(request)
    response.headers["X-Request-Id"] = corr_id
    return response
