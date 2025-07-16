from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxUsageReporterHelper import generate_usage_report

router = APIRouter()

class DropboxUsageReportRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox OAuth access token")
    human_readable: bool = Field(False, description="Return sizes in readable format (e.g. MB, GB)")

@router.post("/dropbox/usage/report")
def dropbox_usage_reporter(request: DropboxUsageReportRequest):
    try:
        return generate_usage_report(
            access_token=request.access_token,
            human_readable=request.human_readable
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))