"""Enterprise Search API — chat over your indexed data, connector admin, files."""

import os
from typing import Any, Dict, Iterator, List, Optional, Union

from .._client import Request, build_body
from .._sse import SSEEvent
from ._types import (
    ConnectorConfig,
    CreateChatSessionResponse,
    RenameChatSessionResponse,
    RunOnceResponse,
    UploadFileResponse,
)

# Accepted inputs for file uploads.
FileInput = Union[str, "os.PathLike[str]", tuple]


def _normalize_files(files: Union[FileInput, List[FileInput]]) -> List[tuple]:
    """Normalise user-supplied files into httpx multipart tuples.

    Accepts a path, a list of paths, or ``(filename, content[, content_type])``
    tuples. All are sent under the ``files`` form field.
    """
    items = files if isinstance(files, list) else [files]
    normalized: List[tuple] = []
    for item in items:
        if isinstance(item, tuple):
            normalized.append(("files", item))
        else:  # treat as a filesystem path
            path = os.fspath(item)
            with open(path, "rb") as fh:
                content = fh.read()
            normalized.append(("files", (os.path.basename(path), content)))
    return normalized


class EnterpriseSearch:
    """Enterprise Search endpoints on the core platform.

    Groups three areas that share the same authenticated context:

    * **Chat** — sessions and messaging over your indexed knowledge
      (``/chat/*``).
    * **Connectors** — admin of data connectors and credential pairs
      (``/manage/admin/*``).
    * **Files** — upload project files for indexing (``/user/projects/file/*``).
    """

    # ------------------------------------------------------------------ chat

    @staticmethod
    def send_chat_message(
        message: str,
        chat_session_id: str,
        *,
        stream: bool = False,
        include_citations: Optional[bool] = None,
        allowed_tool_ids: Optional[List[int]] = None,
        forced_tool_id: Optional[int] = None,
        internal_search_filters: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], Iterator[SSEEvent]]:
        """Send a chat message.

        When ``stream`` is ``True`` this returns an iterator of
        :class:`~chordian.SSEEvent`; otherwise it returns the complete JSON
        response (answer, tool calls, citations, documents).

        :param message: The user message text.
        :param chat_session_id: The chat session UUID (see :meth:`create_chat_session`).
        :param stream: Stream Server-Sent Events instead of a single response.
        :param include_citations: Include citation metadata.
        :param allowed_tool_ids: Permitted tool IDs.
        :param forced_tool_id: Force a specific tool.
        :param internal_search_filters: Search filters (e.g. ``{"source_type": "web"}``).
        """
        body = build_body(
            message=message,
            chat_session_id=chat_session_id,
            stream=stream,
            include_citations=include_citations,
            allowed_tool_ids=allowed_tool_ids,
            forced_tool_id=forced_tool_id,
            internal_search_filters=internal_search_filters,
        )
        request = Request("/chat/send-chat-message", "POST", json=body)
        if stream:
            return request.stream()
        return request.perform()

    @staticmethod
    def get_chat_sessions() -> List[Dict[str, Any]]:
        """List the authenticated user's chat sessions."""
        return Request("/chat/get-user-chat-sessions", "GET").perform()

    @staticmethod
    def create_chat_session(persona_id: int = 0) -> CreateChatSessionResponse:
        """Create a new chat session and return its ID."""
        body = build_body(persona_id=persona_id)
        return Request("/chat/create-chat-session", "POST", json=body).perform()

    @staticmethod
    def rename_chat_session(
        chat_session_id: str, name: str
    ) -> RenameChatSessionResponse:
        """Rename an existing chat session."""
        body = build_body(chat_session_id=chat_session_id, name=name)
        return Request("/chat/rename-chat-session", "PUT", json=body).perform()

    # ------------------------------------------------------------ connectors

    @staticmethod
    def get_connector_status() -> List[Dict[str, Any]]:
        """List connector-credential pairs with status and indexing metrics."""
        return Request("/manage/admin/connector/status", "GET").perform()

    @staticmethod
    def get_connectors(credential: Optional[int] = None) -> List[Dict[str, Any]]:
        """List connectors, optionally filtered by ``credential`` ID."""
        params = {"credential": credential} if credential is not None else None
        return Request("/manage/admin/connector", "GET", params=params).perform()

    @staticmethod
    def create_connector(
        name: str,
        source: str,
        input_type: str,
        *,
        connector_specific_config: Optional[ConnectorConfig] = None,
        refresh_freq: Optional[int] = None,
        prune_freq: Optional[int] = None,
        indexing_start: Optional[str] = None,
        access_type: Optional[str] = None,
        groups: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Create a new connector."""
        body = build_body(
            name=name,
            source=source,
            input_type=input_type,
            connector_specific_config=connector_specific_config,
            refresh_freq=refresh_freq,
            prune_freq=prune_freq,
            indexing_start=indexing_start,
            access_type=access_type,
            groups=groups,
        )
        return Request("/manage/admin/connector", "POST", json=body).perform()

    @staticmethod
    def get_cc_pair(cc_pair_id: int) -> Dict[str, Any]:
        """Get full info for a connector-credential pair."""
        return Request(f"/manage/admin/cc-pair/{cc_pair_id}", "GET").perform()

    @staticmethod
    def update_cc_pair_status(cc_pair_id: int, status: str) -> Dict[str, Any]:
        """Update a connector-credential pair's status.

        :param status: One of ``SCHEDULED``, ``INITIAL_INDEXING``, ``ACTIVE``,
            ``PAUSED``, ``DELETING`` or ``INVALID``.
        """
        body = build_body(status=status)
        return Request(
            f"/manage/admin/cc-pair/{cc_pair_id}/status", "PUT", json=body
        ).perform()

    @staticmethod
    def connector_run_once(
        connector_id: int,
        credential_ids: List[int],
        from_beginning: bool = False,
    ) -> RunOnceResponse:
        """Trigger a one-off indexing run for a connector."""
        body = build_body(
            connector_id=connector_id,
            credential_ids=credential_ids,
            from_beginning=from_beginning,
        )
        return Request("/manage/admin/connector/run-once", "POST", json=body).perform()

    @staticmethod
    def create_deletion_attempt(
        connector_id: int, credential_id: int
    ) -> Dict[str, Any]:
        """Schedule deletion of a connector-credential pair's indexed data."""
        body = build_body(connector_id=connector_id, credential_id=credential_id)
        return Request("/manage/admin/deletion-attempt", "POST", json=body).perform()

    @staticmethod
    def associate_credential(
        connector_id: int,
        credential_id: int,
        *,
        name: Optional[str] = None,
        access_type: Optional[str] = None,
        groups: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Associate a credential with a connector."""
        body = build_body(name=name, access_type=access_type, groups=groups)
        return Request(
            f"/manage/connector/{connector_id}/credential/{credential_id}",
            "PUT",
            json=body,
        ).perform()

    # ----------------------------------------------------------------- files

    @staticmethod
    def upload_file(
        files: Union[FileInput, List[FileInput]]
    ) -> UploadFileResponse:
        """Upload one or more project files for indexing.

        :param files: A path, a list of paths, or ``(filename, content[, type])``
            tuples. Sent as ``multipart/form-data``.
        """
        return Request(
            "/user/projects/file/upload",
            "POST",
            files=_normalize_files(files),
        ).perform()

    @staticmethod
    def get_file_statuses(file_ids: List[str]) -> List[Dict[str, Any]]:
        """Get processing statuses for previously uploaded files."""
        body = build_body(file_ids=file_ids)
        return Request("/user/projects/file/statuses", "POST", json=body).perform()
