import httpx
from app.main import app


async def test_get_games_returns_list():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/games/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
