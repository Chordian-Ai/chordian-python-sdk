"""Type hints for Enterprise Search responses (plain ``dict``s at runtime)."""

from typing import Any, Dict, List

try:
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class CreateChatSessionResponse(TypedDict, total=False):
    chat_session_id: str


class RenameChatSessionResponse(TypedDict, total=False):
    new_name: str


class UserFile(TypedDict, total=False):
    id: str
    name: str
    status: str
    token_count: int
    chunk_count: int


class RejectedFile(TypedDict, total=False):
    file_name: str
    reason: str


class UploadFileResponse(TypedDict, total=False):
    user_files: List[UserFile]
    rejected_files: List[RejectedFile]


class RunOnceResponse(TypedDict, total=False):
    success: bool
    message: str
    data: Any


# A connector_specific_config and the full create-connector body are loosely typed
# because they vary widely by source. Pass plain dicts.
ConnectorConfig = Dict[str, Any]
