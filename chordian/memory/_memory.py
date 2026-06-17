"""Memory / Knowledge Graph API — departments, ingestion and graph chat.

These endpoints live on the **memory service** (a different base URL,
``https://graph-kb.chordian.ai``). The SDK routes them there automatically; the
same API key is used.
"""

import os
from typing import Any, Dict, List, Optional, Union

from .._client import Request, build_body
from ._types import (
    ChatResponse,
    Department,
    DepartmentList,
    GenerateColumn,
    GenerateRecord,
    JobResponse,
)

FileInput = Union[str, "os.PathLike[str]", tuple]


def _normalize_file(file: FileInput) -> tuple:
    """Normalise a single file into an httpx multipart tuple under field ``file``."""
    if isinstance(file, tuple):
        return ("file", file)
    path = os.fspath(file)
    with open(path, "rb") as fh:
        content = fh.read()
    return ("file", (os.path.basename(path), content))


class Memory:
    """Memory / Knowledge Graph endpoints (``/memory/*`` on the memory service).

    Create a *department* (a knowledge graph), feed it data via :meth:`upload`,
    :meth:`ingest_connectors` or :meth:`generate`, then ask questions with
    :meth:`chat`.
    """

    @staticmethod
    def list_departments() -> DepartmentList:
        """List all knowledge-graph departments for the tenant.

        :returns: ``{"departments": [...]}`` — read the ``departments`` key.
        """
        return Request("/memory/departments", "GET", backend="memory").perform()

    @staticmethod
    def get_department(graph_id: str) -> Department:
        """Get a single department by its ``graph_id``."""
        return Request(
            f"/memory/departments/{graph_id}", "GET", backend="memory"
        ).perform()

    @staticmethod
    def create_department(
        name: str,
        *,
        description: Optional[str] = None,
        source_type: Optional[str] = None,
    ) -> Department:
        """Create a new department (knowledge graph)."""
        body = build_body(name=name, description=description, source_type=source_type)
        return Request(
            "/memory/departments/create", "POST", backend="memory", json=body
        ).perform()

    @staticmethod
    def upload(file: FileInput, list_id: str) -> JobResponse:
        """Upload a file to ingest into a department's graph.

        :param file: A path or ``(filename, content[, content_type])`` tuple.
        :param list_id: The target list/department identifier.
        :returns: ``{"jobId", "status", "message"}``.
        """
        return Request(
            "/memory/upload",
            "POST",
            backend="memory",
            files=[_normalize_file(file)],
            data={"list_id": list_id},
        ).perform()

    @staticmethod
    def ingest_connectors(
        list_id: str,
        source_types: Optional[List[str]],
        *,
        mode: Optional[str] = None,
        graph_name: Optional[str] = None,
    ) -> JobResponse:
        """Ingest data from configured connectors into a graph.

        :param list_id: The target list/department identifier.
        :param source_types: Connector source types to ingest (or ``None`` for all).
        :param mode: ``"full"`` or ``"incremental"``.
        :param graph_name: Optional graph name.
        """
        body: Dict[str, Any] = {"list_id": list_id, "source_types": source_types}
        if mode is not None:
            body["mode"] = mode
        if graph_name is not None:
            body["graph_name"] = graph_name
        return Request(
            "/memory/ingest/connectors", "POST", backend="memory", json=body
        ).perform()

    @staticmethod
    def generate(
        list_id: str,
        records: List[GenerateRecord],
        columns: List[GenerateColumn],
        *,
        workflow_category: Optional[str] = None,
    ) -> JobResponse:
        """Generate memory from structured records.

        :param list_id: The target list/department identifier.
        :param records: Rows to ingest (each with ``cells``, ``step_source``, ``metadata``).
        :param columns: Column definitions (each with ``id``, ``header``, ``type``).
        :param workflow_category: Optional workflow category.
        """
        body = build_body(
            listId=list_id,
            records=records,
            columns=columns,
            workflowCategory=workflow_category,
        )
        return Request(
            "/memory/generate", "POST", backend="memory", json=body
        ).perform()

    @staticmethod
    def chat(list_id: str, question: str) -> ChatResponse:
        """Ask a question against a department's knowledge graph.

        :returns: ``{"answer", "nodes", "edges"}``.
        """
        body = build_body(listId=list_id, question=question)
        return Request("/memory/chat", "POST", backend="memory", json=body).perform()
