from typing import List, Optional, Dict, Any
import httpx
from ..core.config import settings

GITHUB_API = "https://api.github.com"

async def _auth_headers() -> dict[str,str]:
    return {"Authorization": f"Bearer {settings.GITHUB_PAT}", "Accept": "application/vnd.github+json"}

async def get_branch_sha(org: str, repo: str, branch: str) -> str:
    url = f"{GITHUB_API}/repos/{org}/{repo}/git/ref/heads/{branch}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=await _auth_headers())
        r.raise_for_status()
        data = r.json()
        return data["object"]["sha"]

async def list_python_scripts(org: str, repo: str, branch: str, prefix: Optional[str]=None, pattern: Optional[str]=None) -> List[Dict[str, Any]]:
    sha = await get_branch_sha(org, repo, branch)
    url = f"{GITHUB_API}/repos/{org}/{repo}/git/trees/{sha}?recursive=1"
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.get(url, headers=await _auth_headers())
        r.raise_for_status()
        items = r.json().get("tree", [])
    blobs = [i for i in items if i.get("type") == "blob" and i.get("path","").endswith(".py")]
    if prefix:
        blobs = [b for b in blobs if b["path"].startswith(prefix.rstrip("/"))]
    if pattern:
        import fnmatch
        blobs = [b for b in blobs if fnmatch.fnmatch(b["path"].split("/")[-1], pattern)]
    result = []
    for b in blobs:
        path = b["path"]
        name = path.split("/")[-1]
        url = f"https://github.com/{org}/{repo}/blob/{branch}/{path}"
        result.append({"name": name, "path": path, "url": url})
    return result
