import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_endpoint_greeting():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/ask", json={"question": "hi"})
    assert response.status_code == 200
    assert "Hello" in response.json()["answer"]


@pytest.mark.asyncio
async def test_ask_endpoint_courses():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/ask", json={"question": "tell me about courses"})
    assert response.status_code == 200
    # The output should contain some course related keywords
    assert any(
        word in response.json()["answer"].lower()
        for word in ["b.tech", "cse", "program", "course"]
    )
