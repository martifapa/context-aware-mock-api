import json

from fastapi import HTTPException, Request, Response, status

from app.repositories.api_repository import ApiRepository
from app.services.state_manager import StateManager


class MockEngine:
    def __init__(self):
        self._repository = ApiRepository()
        self._state_manager = StateManager()

    async def handle(
        self,
        id: str,
        path: str,
        request: Request,
    ) -> Response:
        api_definition = await self._repository.get(id)
        if not api_definition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mock API schema with ID '{id}' could not be found",
            )

        normalized_target_path = f"/{path.strip('/')}" if path else "/"

        matched_route = None
        for route in api_definition.routes:
            normalized_route_path = f"/{route.path.strip('/')}" if route.path else "/"
            if normalized_route_path == normalized_target_path:
                matched_route = route
                break

        if not matched_route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"The path '{normalized_target_path}' is not defined in this "
                    "mock context"
                ),
            )

        request_method = request.method.upper()
        allowed_methods = [m.upper() for m in matched_route.methods]

        if request_method not in allowed_methods:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=(
                    f"Method '{request_method}' is unsupported."
                    f" Allowed: {', '.join(allowed_methods)}"
                ),
            )

        current_state = await self._state_manager.get(id, path)

        default_status = 200
        if request_method == "POST":
            default_status = 201
        elif request_method == "DELETE":
            default_status = 204

        return Response(
            content=json.dumps(current_state),
            status_code=default_status,
            media_type="application/json",
        )
