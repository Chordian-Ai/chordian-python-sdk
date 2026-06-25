"""Web & Research API — Chordian browser research search workflows."""

from typing import Optional

from .._client import Request, build_body
from .._validation import (
    normalize_optional_str,
    require_non_empty_prompt,
    validate_proxy_settings,
)
from ._types import StartResponse
from ._validation import require_web_and_research_llm_model


class WebAndResearch:
    """Web & Research endpoints (``/webandreasearch/*`` on the core platform).

    :meth:`start` bootstraps a Chordian browser research session. Connect to the
    ``websocket_url`` in the response to stream live agent events.
    """

    @staticmethod
    def start(
        prompt: str,
        *,
        live_url: bool,
        proxy: bool,
        llm_model: str,
        thread_id: Optional[str] = None,
        proxy_country_code: Optional[str] = None,
        list_id: Optional[str] = None,
    ) -> StartResponse:
        """Start a web and research search workflow.

        :param prompt: Natural-language search prompt.
        :param live_url: Whether to fetch live URLs.
        :param proxy: Whether to route requests through a proxy.
        :param llm_model: LLM model label (e.g. ``"chordian-r1"``, ``"claude sonnet 4.6"``).
        :param thread_id: Optional existing thread to continue.
        :param proxy_country_code: ISO country code for the proxy; required when
            ``proxy`` is ``True``.
        :param list_id: Optional target list identifier.
        :returns: ``{"success", "message", "thread_id", "list_id", "websocket_url", "status"}``.
        """
        body = build_body(
            prompt=require_non_empty_prompt(prompt),
            live_url=live_url,
            proxy=proxy,
            llm_model=require_web_and_research_llm_model(llm_model),
            thread_id=normalize_optional_str(thread_id),
            proxy_country_code=validate_proxy_settings(
                proxy=proxy,
                proxy_country_code=proxy_country_code,
            ),
            list_id=normalize_optional_str(list_id),
        )
        return Request("/webandreasearch/start", "POST", json=body).perform()
