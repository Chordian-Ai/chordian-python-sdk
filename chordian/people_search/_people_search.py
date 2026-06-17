"""People Search API — find and enrich people via natural-language prompts."""

from typing import Any, Dict, List, Optional

from .._client import Request, build_body
from ._types import ContinueResponse, SearchResponse, StartResponse, StopResponse


class PeopleSearch:
    """People Search endpoints (``/people-search/*`` on the core platform).

    Mirrors :class:`~chordian.CompanySearch`: :meth:`start` an asynchronous
    workflow, poll :meth:`status`, and optionally :meth:`continue_` or enrich.
    Use :meth:`search` for an instant lookup against the people index.
    """

    @staticmethod
    def start(
        prompt: str,
        *,
        list_name: Optional[str] = None,
        list_description: Optional[str] = None,
        search_mode: Optional[str] = None,
    ) -> StartResponse:
        """Start a people search workflow.

        :param prompt: Natural-language description of the people you want.
        :param list_name: Name for the resulting list.
        :param list_description: Human-readable list description.
        :param search_mode: Search mode (e.g. ``"fast"``).
        """
        body = build_body(
            prompt=prompt,
            list_name=list_name,
            list_description=list_description,
            search_mode=search_mode,
        )
        return Request("/people-search/start", "POST", json=body).perform()

    @staticmethod
    def continue_(thread_id: str, total_target: int) -> ContinueResponse:
        """Continue an existing workflow to collect more people."""
        body = build_body(thread_id=thread_id, total_target=total_target)
        return Request("/people-search/continue", "POST", json=body).perform()

    @staticmethod
    def status(thread_id: str) -> Dict[str, Any]:
        """Get a workflow status snapshot (criteria, table structure, progress)."""
        return Request(f"/people-search/status/{thread_id}", "GET").perform()

    @staticmethod
    def stop(thread_id: str) -> StopResponse:
        """Stop a running people search workflow."""
        return Request(f"/people-search/stop/{thread_id}", "POST").perform()

    @staticmethod
    def start_enrichment(thread_id: str, column_name: str) -> Dict[str, Any]:
        """Start enriching a column of the result table.

        :param thread_id: Workflow thread identifier to enrich.
        :param column_name: Column to enrich in the result table.
        """
        body = build_body(thread_id=thread_id, column_name=column_name)
        return Request("/people-search/start-enrichment", "POST", json=body).perform()

    @staticmethod
    def stop_enrichment(thread_id: str) -> Dict[str, Any]:
        """Stop a running enrichment run for ``thread_id``."""
        return Request(
            f"/people-search/stop-enrichment/{thread_id}", "POST"
        ).perform()

    @staticmethod
    def search(
        query: str,
        limit: int,
        path: List[str],
        *,
        fuzzy_max_edits: Optional[int] = None,
    ) -> SearchResponse:
        """Instant search against the people index.

        :param query: Search query (name, email, job title, keyword).
        :param limit: Maximum number of results to return.
        :param path: Searchable field names (e.g. ``["fullName", "emails.email"]``).
        :param fuzzy_max_edits: Maximum edit distance for fuzzy matching.
        """
        body = build_body(
            query=query,
            limit=limit,
            path=path,
            fuzzy_max_edits=fuzzy_max_edits,
        )
        return Request("/people-search/search", "POST", json=body).perform()
