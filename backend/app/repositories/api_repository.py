from app.infrastructure.redis import get_redis_client
from app.models.api_definition import ApiDefinition


class ApiRepository:
    def __init__(self) -> None:
        self._redis = get_redis_client()
        self._key_prefix = "api_definition:"

    def _get_key(self, api_id: str) -> str:
        return f"{self._key_prefix}{api_id}"

    async def save(self, api: ApiDefinition) -> None:
        key = self._get_key(api.api_id)
        api_json = api.model_dump_json()

        await self._redis.set(key, api_json)

    async def get(self, api_id: str) -> ApiDefinition | None:
        key = self._get_key(api_id)
        api_json = self._redis.get(key)

        if not api_json:
            return None

        return ApiDefinition.model_validate_json(api_json)

    async def delete(self, api_id: str) -> None:
        key = self._get_key(api_id)
        await self._redis.delete(key)
