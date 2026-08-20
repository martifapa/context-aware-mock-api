from fastapi import APIRouter, Request

from app.services.mock_engine import MockEngine

router = APIRouter(
    prefix="/mock",
    tags=["mock"],
)

engine = MockEngine()


@router.api_route(
    "/{id}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def mock_endpoint(
    id: str,
    path: str,
    request: Request,
):
    return await engine.handle(id=id, path=path, request=request)
