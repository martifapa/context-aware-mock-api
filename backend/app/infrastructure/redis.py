import redis.asyncio as redis

from app.core.config import settings

pool = redis.ConnectionPool(
  host=settings.redis_host,
  port=settings.redis_port,
  db=settings.redis_db,
  decode_responses=True,
)

def get_redis_client() -> redis.Redis:
    """Returns an active Redis client tied to the connection pool"""
    return redis.Redis(connection_pool=pool)
