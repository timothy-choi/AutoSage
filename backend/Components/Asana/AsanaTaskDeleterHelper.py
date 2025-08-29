import requests
from typing import Dict, Any, List

class AsanaTaskDeleterHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def delete_task(self, task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "message": f"Task {task_gid} deleted."}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def bulk_delete_tasks(self, task_gids: List[str]) -> Dict[str, Any]:
        results = []
        for gid in task_gids:
            result = self.delete_task(gid)
            results.append({gid: result})
        return {"bulk_results": results}