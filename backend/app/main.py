from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.infrastructure.redis import pool

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handles application startup and database connection loops"""
    yield #initialize pool connection on first query
    await pool.disconnect() #close connection on shutdown

app = FastAPI(
    title="Context-Aware Mock API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
