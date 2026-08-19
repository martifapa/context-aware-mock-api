from fastapi import APIRouter, HTTPException, status
from redis.exceptions import RedisError

from app.infrastructure.redis import get_redis_client

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
async def health():
    return {"status": "ok"}


@router.get("/redis")
async def redis_health():
    redis_client = get_redis_client()

    try:
        await redis_client.ping()
        return {"status": "ok", "redis": "pong"}
    except RedisError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Redis connection failed: {str(e)}",
        ) from e
