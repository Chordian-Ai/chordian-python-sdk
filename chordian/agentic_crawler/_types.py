"""Type hints for Agentic Crawler responses."""

from typing import TypedDict


class StartResponse(TypedDict, total=False):
    success: bool
    message: str
    thread_id: str
    list_id: str
    websocket_url: str
    status: str
