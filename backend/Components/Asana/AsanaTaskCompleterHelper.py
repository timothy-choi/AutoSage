import requests
from typing import Dict, Any, List

class AsanaTaskCompleterHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def complete_task(self, task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}"
        data = {"data": {"completed": True}}
        resp = requests.put(url, headers=self.headers, json=data)

        if resp.status_code == 200:
            return {"success": True, "message": f"Task {task_gid} marked as completed."}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def uncomplete_task(self, task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}"
        data = {"data": {"completed": False}}
        resp = requests.put(url, headers=self.headers, json=data)

        if resp.status_code == 200:
            return {"success": True, "message": f"Task {task_gid} marked as incomplete."}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def bulk_complete_tasks(self, task_gids: List[str]) -> Dict[str, Any]:
        results = []
        for gid in task_gids:
            result = self.complete_task(gid)
            results.append({gid: result})
        return {"bulk_results": results}

    def bulk_uncomplete_tasks(self, task_gids: List[str]) -> Dict[str, Any]:
        results = []
        for gid in task_gids:
            result = self.uncomplete_task(gid)
            results.append({gid: result})
        return {"bulk_results": results}