from unittest.mock import AsyncMock

from fastapi import HTTPException

from app.api.routes.mock import engine, mock_endpoint
from app.main import app


async def test_get_mock_endpoint(client, monkeypatch):
    """A correct GET request goes through correctly."""

    mock_response = {"status": "ok", "data": {"message": "mocked"}}
    mock_handle = AsyncMock(return_value=mock_response)

    monkeypatch.setattr(engine, "handle", mock_handle)

    response = await client.get("/mock/example-id/users/profile")

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_handle.assert_awaited_once()

    call = mock_handle.await_args
    assert call.kwargs["id"] == "example-id"
    assert call.kwargs["path"] == "users/profile"
    assert call.kwargs["request"] is not None
    assert mock_endpoint is not None
    assert app is not None


async def test_get_mock_endpoint_without_api_definition_returns_404(
    client,
    monkeypatch,
):
    """A request without an ApiDefinition returns HTTP 404."""

    mock_handle = AsyncMock(
        side_effect=HTTPException(
            status_code=404,
            detail="ApiDefinition not found",
        )
    )
    monkeypatch.setattr(engine, "handle", mock_handle)

    response = await client.get("/mock/missing-api/users")

    assert response.status_code == 404


async def test_get_mock_endpoint_without_matching_route_returns_404(
    client,
    monkeypatch,
):
    """A request without a matching RouteDefinition returns HTTP 404."""

    mock_handle = AsyncMock(
        side_effect=HTTPException(
            status_code=404,
            detail="RouteDefinition not found",
        )
    )
    monkeypatch.setattr(engine, "handle", mock_handle)

    response = await client.get("/mock/example-id/missing-route")

    assert response.status_code == 404


async def test_mock_endpoint_with_unsupported_method_returns_405(client):
    """A request using an unsupported HTTP method returns HTTP 405."""
    
    response = await client.head("/mock/example-id/users/profile")

    assert response.status_code == 405