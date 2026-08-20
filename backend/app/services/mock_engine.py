import json

from fastapi import HTTPException, Request, Response, status

from app.repositories.api_repository import ApiRepository


class MockEngine:

    def __init__(self):
            self._repository = ApiRepository()

    async def handle(
        self,
        api_id: str,
        path: str,
        request: Request,
    ) -> Response:
        api_definition = await self._repository.get(api_id)
        if not api_definition:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Mock API schema with ID '{api_id}' could not be found",
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

        return Response(
             content=json.dumps(matched_route.response_body),
             status_code=matched_route.response_status,
             media_type="application/json",
        )
