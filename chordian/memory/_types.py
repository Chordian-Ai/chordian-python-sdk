"""Type hints for Memory / Knowledge Graph payloads and responses."""

from typing import Any, Dict, List

try:
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class Department(TypedDict, total=False):
    graph_id: str
    name: str
    description: str
    created_at: str
    updated_at: str
    node_count: int
    edge_count: int
    source_type: str
    status: str
    tenant_id: str
    list_id: str


class DepartmentList(TypedDict, total=False):
    departments: List[Department]


class JobResponse(TypedDict, total=False):
    jobId: str
    status: str
    message: str


class ChatResponse(TypedDict, total=False):
    answer: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class GenerateColumn(TypedDict, total=False):
    id: str
    header: str
    type: str


class GenerateRecord(TypedDict, total=False):
    cells: Dict[str, Any]
    step_source: str
    metadata: Dict[str, Any]
