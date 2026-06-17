"""Company Search API — find and enrich companies via natural-language prompts."""

from typing import Any, Dict, List, Optional

from .._client import Request, build_body
from ._types import (
    ContinueResponse,
    ListsResponse,
    SearchResponse,
    SearchResultResponse,
    StartResponse,
    StopResponse,
)


class CompanySearch:
    """Company Search endpoints (``/company-search/*`` on the core platform).

    A typical workflow is asynchronous: :meth:`start` a search, poll
    :meth:`status` until it completes, then read :meth:`get_search_result`. Use
    :meth:`search` for an instant lookup against the existing company index.
    """

    @staticmethod
    def start(
        prompt: str,
        *,
        list_name: Optional[str] = None,
        list_description: Optional[str] = None,
        search_mode: Optional[str] = None,
    ) -> StartResponse:
        """Start a company search workflow.

        :param prompt: Natural-language description of the companies you want.
        :param list_name: Name for the resulting list.
        :param list_description: Human-readable list description.
        :param search_mode: Search mode (e.g. ``"fast"``).
        :returns: ``{"success", "message", "thread_id", "status"}``.
        """
        body = build_body(
            prompt=prompt,
            list_name=list_name,
            list_description=list_description,
            search_mode=search_mode,
        )
        return Request("/company-search/start", "POST", json=body).perform()

    @staticmethod
    def continue_(thread_id: str, total_target: int) -> ContinueResponse:
        """Continue an existing workflow to collect more companies.

        :param thread_id: The workflow thread identifier from :meth:`start`.
        :param total_target: Target total number of companies to collect.
        """
        body = build_body(thread_id=thread_id, total_target=total_target)
        return Request("/company-search/continue", "POST", json=body).perform()

    @staticmethod
    def status(task_id: str) -> Dict[str, Any]:
        """Get a workflow status snapshot (criteria, rows, progress counters).

        :param task_id: The workflow thread id returned by :meth:`start`.
        """
        return Request(f"/company-search/status/{task_id}", "GET").perform()

    @staticmethod
    def stop(thread_id: str) -> StopResponse:
        """Stop a running company search workflow."""
        return Request(f"/company-search/stop/{thread_id}", "POST").perform()

    @staticmethod
    def start_enrichment(
        thread_id: str,
        column_name: str,
        *,
        instruction: Optional[str] = None,
        enrichment_type: Optional[str] = None,
        data_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start enriching a column of the result table.

        :param thread_id: Workflow thread identifier.
        :param column_name: Target column to enrich.
        :param instruction: Natural-language enrichment instruction.
        :param enrichment_type: Enrichment variant (e.g. ``"custom"``).
        :param data_type: Data type hint (e.g. ``"company"``).
        """
        body = build_body(
            thread_id=thread_id,
            column_name=column_name,
            instruction=instruction,
            enrichment_type=enrichment_type,
            data_type=data_type,
        )
        return Request("/company-search/start-enrichment", "POST", json=body).perform()

    @staticmethod
    def stop_enrichment(thread_id: str) -> Dict[str, Any]:
        """Stop a running enrichment for ``thread_id``."""
        return Request(
            f"/company-search/stop-enrichment/{thread_id}", "POST"
        ).perform()

    @staticmethod
    def get_lists() -> ListsResponse:
        """List the company lists saved for the authenticated tenant."""
        return Request("/company-search/getLists", "GET").perform()

    @staticmethod
    def get_search_result(thread_id: str) -> SearchResultResponse:
        """Get the full result (criteria + rows) for a completed workflow."""
        return Request(
            f"/company-search/getSearchResult/{thread_id}", "GET"
        ).perform()

    @staticmethod
    def search(
        query: str,
        limit: int,
        path: List[str],
        *,
        fuzzy_max_edits: Optional[int] = None,
    ) -> SearchResponse:
        """Instant search against the company index.

        :param query: Search query (domain, company name, keyword).
        :param limit: Maximum number of results to return.
        :param path: Searchable field names (e.g. ``["website", "companyName"]``).
        :param fuzzy_max_edits: Maximum edit distance for fuzzy matching.
        """
        body = build_body(
            query=query,
            limit=limit,
            path=path,
            fuzzy_max_edits=fuzzy_max_edits,
        )
        return Request("/company-search/search", "POST", json=body).perform()
