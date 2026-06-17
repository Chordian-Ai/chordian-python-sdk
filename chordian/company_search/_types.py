"""Type hints for Company Search responses.

These ``TypedDict``s document the shapes returned by the API. Responses are plain
``dict``s at runtime and may contain additional keys, so treat them as guidance.
"""

from typing import Any, Dict, List

try:  # TypedDict lives in typing from 3.8, but use typing_extensions if needed.
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class StartResponse(TypedDict, total=False):
    success: bool
    message: str
    thread_id: str
    status: str


class ContinueResponse(TypedDict, total=False):
    success: bool
    thread_id: str
    status: str


class StopResponse(TypedDict, total=False):
    success: bool
    thread_id: str
    status: str
    message: str


class ListsResponse(TypedDict, total=False):
    success: bool
    data: List[Dict[str, Any]]
    total: int


class SearchResponse(TypedDict, total=False):
    results: List[Dict[str, Any]]
    count: int


class SearchResultResponse(TypedDict, total=False):
    success: bool
    thread_id: str
    list_id: str
    status: str
    list_name: str
    list_description: str
    list_type: str
    total_target: int
    criteria: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    count: int
    created_at: str
    updated_at: str
