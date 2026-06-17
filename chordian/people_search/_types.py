"""Type hints for People Search responses (plain ``dict``s at runtime)."""

from typing import Any, Dict, List

try:
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


class PersonEmail(TypedDict, total=False):
    email: str
    smtp_valid: str
    last_validation_check: str


class Person(TypedDict, total=False):
    _id: str
    firstName: str
    lastName: str
    fullName: str
    position: List[str]
    personalInfo: Dict[str, Any]
    recommended_email: List[str]
    emails: List[PersonEmail]
    experiences: List[Dict[str, Any]]
    education: List[Dict[str, Any]]


class SearchResponse(TypedDict, total=False):
    results: List[Person]
    count: int
