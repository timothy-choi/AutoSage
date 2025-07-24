from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List
from ConfluenceLabelManagerHelper import (
    add_labels_to_confluence_page,
    get_labels_of_confluence_page,
    remove_label_from_confluence_page,
)

router = APIRouter()

class LabelRequest(BaseModel):
    base_url: str
    username: str
    api_token: str
    page_id: str
    labels: List[str]

class RemoveLabelRequest(BaseModel):
    base_url: str
    username: str
    api_token: str
    page_id: str
    label: str

class LabelFetchRequest(BaseModel):
    base_url: str
    username: str
    api_token: str
    page_id: str

@router.post("/confluence/page/labels/add")
def add_labels(request: LabelRequest):
    return add_labels_to_confluence_page(
        base_url=request.base_url,
        username=request.username,
        api_token=request.api_token,
        page_id=request.page_id,
        labels=request.labels
    )

@router.post("/confluence/page/labels/remove")
def remove_label(request: RemoveLabelRequest):
    return remove_label_from_confluence_page(
        base_url=request.base_url,
        username=request.username,
        api_token=request.api_token,
        page_id=request.page_id,
        label=request.label
    )

@router.post("/confluence/page/labels/get")
def get_labels(request: LabelFetchRequest):
    return get_labels_of_confluence_page(
        base_url=request.base_url,
        username=request.username,
        api_token=request.api_token,
        page_id=request.page_id
    )