from fastapi import APIRouter, Query, HTTPException
from VideoSharerHelper import generate_shareable_link, get_token_metadata, validate_token
import os

router = APIRouter()

@router.get("/video/share-link")
def get_shareable_link(filename: str = Query(...)):
    try:
        file_path = os.path.join("shared_videos", filename)
        link = generate_shareable_link(file_path)
        return {"link": link}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/share-metadata")
def get_share_metadata(filename: str = Query(...)):
    try:
        file_path = os.path.join("shared_videos", filename)
        metadata = get_token_metadata(file_path)
        return metadata
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video/validate-token")
def validate_share_token(filename: str = Query(...), token: str = Query(...)):
    try:
        file_path = os.path.join("shared_videos", filename)
        valid = validate_token(file_path, token)
        return {"valid": valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))