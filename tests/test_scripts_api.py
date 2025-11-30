import pytest, respx, httpx
from fastapi import FastAPI
from app.api.v1.scripts import router
from app.core.config import settings

@pytest.mark.asyncio
async def test_scripts_listing():
    app = FastAPI()
    app.include_router(router)
    sha = "abc123"
    with respx.mock:
        respx.get(f"https://api.github.com/repos/{settings.GITHUB_ORG}/{settings.GITHUB_REPO}/git/ref/heads/{settings.GITHUB_BRANCH}").mock(return_value=httpx.Response(200, json={"object":{"sha": sha}}))
        respx.get(f"https://api.github.com/repos/{settings.GITHUB_ORG}/{settings.GITHUB_REPO}/git/trees/{sha}?recursive=1").mock(return_value=httpx.Response(200, json={"tree":[
            {"path":"tools/a.py","type":"blob"},{"path":"README.md","type":"blob"}
        ]}))
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            r = await ac.get("/scripts")
            assert r.status_code == 200
            data = r.json()
            assert data and data[0]["name"] == "a.py"
