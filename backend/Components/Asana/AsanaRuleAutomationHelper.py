import requests
from typing import Dict, List, Optional


class AsanaRuleAutomationHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def search_tasks(self, workspace_gid: str, filters: Dict) -> List[Dict]:
        url = f"{self.base_url}/workspaces/{workspace_gid}/tasks/search"
        resp = requests.get(url, headers=self.headers, params=filters)
        return resp.json().get("data", []) if resp.status_code == 200 else []

    def move_task_to_section(self, task_gid: str, section_gid: str) -> Dict:
        url = f"{self.base_url}/sections/{section_gid}/addTask"
        payload = {"data": {"task": task_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def assign_task(self, task_gid: str, user_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        payload = {"data": {"assignee": user_gid}}
        resp = requests.put(url, headers=self.headers, json=payload)
        return resp.json()

    def add_comment_to_task(self, task_gid: str, text: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/stories"
        payload = {"data": {"text": text}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def mark_task_complete(self, task_gid: str) -> Dict:
        """Mark a task complete (rule action)."""
        url = f"{self.base_url}/tasks/{task_gid}"
        payload = {"data": {"completed": True}}
        resp = requests.put(url, headers=self.headers, json=payload)
        return resp.json()

    def run_rule(self, workspace_gid: str, filters: Dict, actions: List[Dict]) -> List[Dict]:
        matched_tasks = self.search_tasks(workspace_gid, filters)
        results = []

        for task in matched_tasks:
            task_gid = task["gid"]
            for action in actions:
                if action["type"] == "assign":
                    results.append(self.assign_task(task_gid, action["user_gid"]))
                elif action["type"] == "move":
                    results.append(self.move_task_to_section(task_gid, action["section_gid"]))
                elif action["type"] == "comment":
                    results.append(self.add_comment_to_task(task_gid, action["text"]))
                elif action["type"] == "complete":
                    results.append(self.mark_task_complete(task_gid))

        return results