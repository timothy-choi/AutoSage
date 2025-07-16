import httpx
import os

FIGMA_API_BASE = "https://api.figma.com/v1"
FIGMA_PERSONAL_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")

HEADERS = {
    "X-Figma-Token": FIGMA_PERSONAL_ACCESS_TOKEN
}

async def create_figma_team_project(team_id: str, project_name: str):
    url = f"{FIGMA_API_BASE}/teams/{team_id}/projects"
    payload = {"name": project_name}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()

async def list_team_projects(team_id: str):
    url = f"{FIGMA_API_BASE}/teams/{team_id}/projects"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def rename_project(project_id: str, new_name: str):
    url = f"{FIGMA_API_BASE}/projects/{project_id}"
    payload = {"name": new_name}
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()

async def delete_project(project_id: str):
    url = f"{FIGMA_API_BASE}/projects/{project_id}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=HEADERS)
        if response.status_code == 204:
            return {"status": "success", "message": "Project deleted"}
        else:
            response.raise_for_status()

async def get_project_details(project_id: str):
    url = f"{FIGMA_API_BASE}/projects/{project_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()