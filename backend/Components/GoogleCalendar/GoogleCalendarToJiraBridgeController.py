from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from GoogleCalendarToJiraBridgeHelper import push_calendar_events_to_jira

router = APIRouter()

class CalendarToJiraRequest(BaseModel):
    google_access_token: str = Field(..., description="Google OAuth token")
    calendar_id: str = Field("primary", description="Google Calendar ID")
    jira_base_url: str = Field(..., description="Base URL of Jira instance")
    jira_email: str = Field(..., description="Email used for Jira auth")
    jira_api_token: str = Field(..., description="Jira API token")
    jira_project_key: str = Field(..., description="Jira project key")
    hours_ahead: Optional[int] = Field(24, description="Time window (hours)")
    max_results: Optional[int] = Field(10, description="Max number of events to sync")

@router.post("/gcalendar/to-jira")
def calendar_to_jira(request: CalendarToJiraRequest):
    try:
        return push_calendar_events_to_jira(
            google_access_token=request.google_access_token,
            calendar_id=request.calendar_id,
            jira_base_url=request.jira_base_url,
            jira_email=request.jira_email,
            jira_api_token=request.jira_api_token,
            jira_project_key=request.jira_project_key,
            hours_ahead=request.hours_ahead,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))