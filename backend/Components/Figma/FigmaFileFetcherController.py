from fastapi import APIRouter, Query
from FigmaFileFetcherHelper import (
    fetch_file_metadata,
    fetch_file_nodes,
    download_node_images
)

router = APIRouter()

@router.get("/figma/file/metadata")
async def get_file_metadata(file_key: str = Query(..., description="Figma file key")):
    return await fetch_file_metadata(file_key)

@router.get("/figma/file/nodes")
async def get_file_nodes(
    file_key: str = Query(..., description="Figma file key"),
    node_ids: str = Query(..., description="Comma-separated list of node IDs")
):
    return await fetch_file_nodes(file_key, node_ids)

@router.get("/figma/file/images")
async def get_file_images(
    file_key: str = Query(..., description="Figma file key"),
    node_ids: str = Query(..., description="Comma-separated list of node IDs"),
    format: str = Query("png", description="Image format: png, jpg, svg")
):
    return await download_node_images(file_key, node_ids, format)