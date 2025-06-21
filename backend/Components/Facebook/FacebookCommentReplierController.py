from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from FacebookCommentReplierHelper import (
    reply_to_comment,
    batch_reply_to_comments,
    keyword_reply,
    delete_comment,
    edit_comment
)

app = FastAPI()


class ReplyRequest(BaseModel):
    comment_id: str
    message: str
    access_token: str


class BatchReplyRequest(BaseModel):
    comment_ids: List[str]
    message: str
    access_token: str


class KeywordReplyRequest(BaseModel):
    comment_id: str
    comment_text: str
    keyword_reply_map: Dict[str, str]
    access_token: str


class EditRequest(BaseModel):
    comment_id: str
    new_message: str
    access_token: str


class DeleteRequest(BaseModel):
    comment_id: str
    access_token: str


@app.post("/facebook/reply")
def reply(request: ReplyRequest):
    return reply_to_comment(request.comment_id, request.message, request.access_token)


@app.post("/facebook/batch-reply")
def batch_reply(request: BatchReplyRequest):
    return batch_reply_to_comments(request.comment_ids, request.message, request.access_token)


@app.post("/facebook/keyword-reply")
def keyword_reply_route(request: KeywordReplyRequest):
    return keyword_reply(request.comment_id, request.comment_text, request.keyword_reply_map, request.access_token)


@app.post("/facebook/edit-comment")
def edit(request: EditRequest):
    return edit_comment(request.comment_id, request.new_message, request.access_token)


@app.post("/facebook/delete-comment")
def delete(request: DeleteRequest):
    return delete_comment(request.comment_id, request.access_token)