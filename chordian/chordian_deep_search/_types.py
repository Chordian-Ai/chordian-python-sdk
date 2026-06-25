"""Type hints for Chordian Deep Search responses."""

from typing import List, TypedDict


class StartResponse(TypedDict, total=False):
    success: bool
    thread_id: str
    list_id: str
    websocket_url: str
    live_url: str
    workspace_id: str
    status: str


class UploadResponse(TypedDict, total=False):
    success: bool
    workspace_id: str
    paths: List[str]
