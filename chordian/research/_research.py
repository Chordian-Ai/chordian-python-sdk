"""Deep Research API — multi-agent research workflows with streaming progress."""

from typing import Any, Dict, Iterator, List, Optional

from .._client import Request, build_body
from .._sse import SSEEvent
from ._types import StartResponse


def _resolve_service_id(service_id: Optional[str]) -> str:
    import chordian

    resolved = service_id or chordian.service_id
    if not resolved:
        raise ValueError(
            "Deep Research requires a service ID for credit tracking. Pass "
            "`service_id=...` or set `chordian.service_id = \"...\"`."
        )
    return resolved


class Research:
    """Deep Research endpoints (``/research/*`` on the core platform).

    Workflow: :meth:`start` a research run (optionally allowing clarifying
    questions), then either :meth:`stream` live progress events or poll
    :meth:`status`. If the agent asks a clarifying question, reply with
    :meth:`respond`. The final report is delivered on the ``complete`` stream
    event and via :meth:`status` once finished.
    """

    @staticmethod
    def start(
        query: str,
        *,
        service_id: Optional[str] = None,
        allow_clarification: Optional[bool] = None,
        max_concurrent_research_units: Optional[int] = None,
        max_researcher_iterations: Optional[int] = None,
        tenant_id: Optional[str] = None,
    ) -> StartResponse:
        """Start a deep research workflow.

        :param query: The research question.
        :param service_id: Service ID for credit checking (required; falls back
            to ``chordian.service_id``).
        :param allow_clarification: Allow the agent to ask clarifying questions.
        :param max_concurrent_research_units: Max concurrent research agents.
        :param max_researcher_iterations: Max iterations per researcher.
        :param tenant_id: Optional tenant identifier.
        """
        body = build_body(
            query=query,
            serviceId=_resolve_service_id(service_id),
            allow_clarification=allow_clarification,
            max_concurrent_research_units=max_concurrent_research_units,
            max_researcher_iterations=max_researcher_iterations,
            tenant_id=tenant_id,
        )
        return Request("/research/start", "POST", json=body).perform()

    @staticmethod
    def stream(thread_id: str) -> Iterator[SSEEvent]:
        """Stream research progress as Server-Sent Events.

        Yields :class:`~chordian.SSEEvent` objects for clarification, progress and
        completion. Use ``event.json`` to parse each payload::

            for event in chordian.Research.stream(thread_id):
                print(event.event, event.json)
        """
        return Request(f"/research/stream/{thread_id}", "GET").stream()

    @staticmethod
    def status(thread_id: str) -> Dict[str, Any]:
        """Get the current status (and final report, when finished)."""
        return Request(f"/research/status/{thread_id}", "GET").perform()

    @staticmethod
    def active() -> List[Dict[str, Any]]:
        """List the active research workflows for the authenticated tenant."""
        return Request("/research/active", "GET").perform()

    @staticmethod
    def respond(thread_id: str, response: str) -> Dict[str, Any]:
        """Reply to a clarifying question and resume the workflow.

        :param thread_id: The research thread awaiting clarification.
        :param response: Your answer to the clarifying question.
        """
        return Request(
            f"/research/respond/{thread_id}",
            "POST",
            params={"response": response},
        ).perform()

    @staticmethod
    def stop(thread_id: str) -> Dict[str, Any]:
        """Stop a running research workflow."""
        return Request(f"/research/stop/{thread_id}", "DELETE").perform()
