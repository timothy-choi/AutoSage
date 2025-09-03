import requests
from typing import Dict

class AsanaTeamManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def list_teams_in_workspace(self, workspace_gid: str) -> Dict:
        url = f"{self.base_url}/organizations/{workspace_gid}/teams"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "teams": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_team(self, team_gid: str) -> Dict:
        url = f"{self.base_url}/teams/{team_gid}"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "team": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_users_in_team(self, team_gid: str) -> Dict:
        url = f"{self.base_url}/teams/{team_gid}/users"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "users": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def add_user_to_team(self, team_gid: str, user_gid: str) -> Dict:
        url = f"{self.base_url}/team_memberships"
        payload = {"data": {"team": team_gid, "user": user_gid}}
        resp = requests.post(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)

        if resp.status_code in [200, 201]:
            return {"success": True, "membership": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def remove_user_from_team(self, membership_gid: str) -> Dict:
        url = f"{self.base_url}/team_memberships/{membership_gid}"
        resp = requests.delete(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "message": "User removed from team"}
        return {"success": False, "status": resp.status_code, "details": resp.text}