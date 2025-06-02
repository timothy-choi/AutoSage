from fastapi import APIRouter, Query, HTTPException
from EmbedVideoCodeGeneratorHelper import (
    generate_embed_code,
    generate_markdown_embed,
    is_valid_url,
    generate_js_player_embed,
    generate_videojs_embed
)

router = APIRouter()

@router.get("/embed/iframe")
def get_iframe_embed(video_url: str, width: int = 640, height: int = 360, autoplay: bool = False):
    if not is_valid_url(video_url):
        raise HTTPException(status_code=400, detail="Invalid video URL")
    return {"embed_code": generate_embed_code(video_url, width, height, autoplay)}

@router.get("/embed/markdown")
def get_markdown_embed(video_url: str, alt_text: str = "Video"):
    if not is_valid_url(video_url):
        raise HTTPException(status_code=400, detail="Invalid video URL")
    return {"markdown": generate_markdown_embed(video_url, alt_text)}

@router.get("/embed/js")
def get_js_embed(video_url: str, player_id: str = "video-player"):
    if not is_valid_url(video_url):
        raise HTTPException(status_code=400, detail="Invalid video URL")
    return {"html": generate_js_player_embed(video_url, player_id)}

@router.get("/embed/videojs")
def get_videojs_embed(video_url: str, width: int = 640, height: int = 360, player_id: str = "videojs-player"):
    if not is_valid_url(video_url):
        raise HTTPException(status_code=400, detail="Invalid video URL")
    return {"html": generate_videojs_embed(video_url, width, height, player_id)}