"""Agentic Crawler API — browser-based agentic search workflows."""

from typing import Optional

from .._client import Request, build_body
from .._validation import normalize_optional_str, require_non_empty_prompt
from ._types import StartResponse


class AgenticCrawler:
    """Agentic Crawler endpoints (``/agentic-crawler/*`` on the core platform).

    :meth:`start` bootstraps a browser search session. Connect to the
    ``websocket_url`` in the response to stream live agent events.
    """

    @staticmethod
    def start(
        prompt: str,
        *,
        thread_id: Optional[str] = None,
        list_id: Optional[str] = None,
    ) -> StartResponse:
        """Start an agentic crawler workflow.

        :param prompt: Natural-language search or crawl prompt.
        :param thread_id: Optional existing thread to continue.
        :param list_id: Optional target list identifier.
        :returns: ``{"success", "message", "thread_id", "list_id", "websocket_url", "status"}``.
        """
        body = build_body(
            prompt=require_non_empty_prompt(prompt),
            thread_id=normalize_optional_str(thread_id),
            list_id=normalize_optional_str(list_id),
        )
        return Request("/agentic-crawler/start", "POST", json=body).perform()
