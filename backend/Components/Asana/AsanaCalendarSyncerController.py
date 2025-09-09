from fastapi import APIRouter
from typing import Dict
from AsanaCalendarSyncerHelper import AsanaCalendarSyncerHelper

router = APIRouter()
helper_instances = {}

def get_helper(token: str) -> AsanaCalendarSyncerHelper:
    if token not in helper_instances:
        helper_instances[token] = AsanaCalendarSyncerHelper(token)
    return helper_instances[token]

@router.get("/asana/project/{project_gid}/calendar/sync")
def sync_project_calendar(token: str, project_gid: str, limit: int = 20) -> Dict:
    helper = get_helper(token)
    tasks = helper.fetch_upcoming_tasks(project_gid, limit)
    events = helper.convert_to_calendar_events(tasks)
    return helper.push_to_external_calendar(events)