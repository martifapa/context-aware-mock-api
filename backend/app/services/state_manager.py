import json

from app.infrastructure.redis import get_redis_client
from app.models.route_definition import RouteDefinition


class StateManager:
    def __init__(self):
        self._redis = get_redis_client()
        self._prefix = "mock_state"

    def _get_key(self, api_id: str, route_path: str) -> str:
        clean_path = route_path.strip("/")
        return f"{self._prefix}:{api_id}:{clean_path}"

    async def initialize(
        self,
        api_id: str,
        route: RouteDefinition,
        data: list[dict],
    ) -> None:
        key = self._get_key(api_id, route.path)

        exists = await self._redis.exists(key)
        if not exists:
            await self.replace(api_id, route.path, data)

    async def get(self, api_id: str, route_path: str) -> list[dict]:
        key = self._get_key(api_id, route_path)
        raw_data = await self._redis.get(key)

        if not raw_data:
            return []

        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return []

    async def replace(
        self,
        api_id: str,
        route_path: str,
        data: list[dict],
    ) -> None:
        key = self._get_key(api_id, route_path)

        serialized_data = json.dumps(data)
        await self._redis.set(key, serialized_data)
