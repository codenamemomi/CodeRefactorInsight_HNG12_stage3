import pytest
from httpx import AsyncClient
from main import app  # Assuming your file is named main.py

@pytest.mark.asyncio
async def test_fetch_github_commits():
    from main import fetch_github_commits
    
    owner = "octocat"
    repo = "Hello-World"
    commits = await fetch_github_commits(owner, repo)
    
    assert isinstance(commits, list) or "error" in commits

@pytest.mark.asyncio
async def test_handle_tick():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "channel_id": "test_channel",
            "return_url": "http://example.com",
            "settings": [
                {"label": "Github_username", "type": "text", "required": True, "default": "octocat"},
                {"label": "Github_repo", "type": "text", "required": True, "default": "Hello-World"}
            ]
        }
        response = await client.post("/tick", json=payload)
        assert response.status_code == 202
        assert response.json()["status"] == "accepted"

@pytest.mark.asyncio
async def test_get_integration_json():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/integration.json")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["descriptions"]["app_name"] == "Code Refactor Insight"
