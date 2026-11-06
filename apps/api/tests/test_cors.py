from httpx import AsyncClient


async def test_cors_allows_frontend_origin(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"Origin": "http://localhost:5173"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


async def test_cors_blocks_unknown_origin(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"Origin": "http://evil.example"})

    assert "access-control-allow-origin" not in response.headers
