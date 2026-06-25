"""Chordian Deep Search API — live cloud-browser deep search workflows."""

import os
from typing import Any, Dict, Optional, Union

from .._client import Request, build_body
from .._validation import (
    normalize_optional_str,
    require_non_empty_prompt,
    validate_proxy_settings,
)
from ._types import StartResponse, UploadResponse

FileInput = Union[str, "os.PathLike[str]", tuple]


def _normalize_file(file: FileInput) -> tuple:
    """Normalise a single file into an httpx multipart tuple under field ``file``."""
    if isinstance(file, tuple):
        return ("file", file)
    path = os.fspath(file)
    with open(path, "rb") as fh:
        content = fh.read()
    return ("file", (os.path.basename(path), content))


class ChordianDeepSearch:
    """Chordian Deep Search endpoints (``/chordian-deep-search/*`` on the core platform).

    :meth:`start` begins a live cloud-browser deep search run. Connect to the
    ``websocket_url`` in the response for browser activity and chat events.
    Use :meth:`upload` to add files to the session workspace.
    """

    @staticmethod
    def start(
        prompt: str,
        *,
        thread_id: Optional[str] = None,
        list_id: Optional[str] = None,
        llm_model: Optional[str] = None,
        live_url: Optional[bool] = None,
        proxy: Optional[bool] = None,
        proxy_country_code: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> StartResponse:
        """Start a Chordian deep search workflow.

        :param prompt: Natural-language search prompt.
        :param thread_id: Optional existing thread to continue.
        :param list_id: Optional target list identifier.
        :param llm_model: Browser v3 cloud model id (e.g. ``"claude-sonnet-4.6"``).
            Legacy web & research labels are accepted by the server.
        :param live_url: Whether to use a live cloud browser (default ``True`` on server).
        :param proxy: Whether to route through a proxy.
        :param proxy_country_code: ISO country code for the proxy; required when
            ``proxy`` is ``True``.
        :param workspace_id: Optional workspace id for file-based chat.
        :returns: ``{"success", "thread_id", "list_id", "websocket_url", "live_url", "workspace_id", "status"}``.
        """
        normalized_proxy = proxy if proxy is not None else False
        normalized_live_url = live_url if live_url is not None else True
        body = build_body(
            prompt=require_non_empty_prompt(prompt),
            thread_id=normalize_optional_str(thread_id),
            list_id=normalize_optional_str(list_id),
            llm_model=normalize_optional_str(llm_model),
            live_url=live_url,
            proxy=proxy,
            proxy_country_code=validate_proxy_settings(
                proxy=normalized_proxy,
                live_url=normalized_live_url,
                proxy_country_code=proxy_country_code,
                require_live_url_when_proxy=True,
            ),
            workspace_id=normalize_optional_str(workspace_id),
        )
        return Request("/chordian-deep-search/start", "POST", json=body).perform()

    @staticmethod
    def upload(
        file: FileInput,
        *,
        thread_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a file into a deep search cloud-browser workspace.

        :param file: A path or ``(filename, content[, content_type])`` tuple.
        :param thread_id: Thread id from :meth:`start`.
        :param workspace_id: Optional workspace id.
        :returns: ``{"success", "workspace_id", "paths", ...}``.
        """
        data = build_body(
            thread_id=normalize_optional_str(thread_id),
            workspace_id=normalize_optional_str(workspace_id),
        )
        return Request(
            "/chordian-deep-search/upload",
            "POST",
            files=[_normalize_file(file)],
            data=data or None,
        ).perform()
