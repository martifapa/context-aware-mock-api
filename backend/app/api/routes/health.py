from fastapi import APIRouter

from app.infrastructure.redis import redis_client

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
async def health():
    return {"status": "ok"}


@router.get("/redis")
async def redis_health():
    await redis_client.ping()

    return {"status": "ok", "redis": "pong"}
