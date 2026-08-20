from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/mock",
  tags=["mock"],
)


@router.api_route(
  "/{api_id}/{path:path}",
  methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def mock_endpoint(
  api_id: str,
  path: str,
  request: Request,
):
    return {"api_id": api_id, "path": path}