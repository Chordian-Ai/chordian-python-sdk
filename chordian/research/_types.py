"""Type hints for Deep Research responses (plain ``dict``s at runtime)."""

try:
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class StartResponse(TypedDict, total=False):
    thread_id: str
    status: str
    message: str
    research_brief: str
    final_report: str
