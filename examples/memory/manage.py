"""Memory: list/inspect departments and ingest connector data.

Covers list_departments, get_department and ingest_connectors.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/manage.py [list_id]
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    # List all knowledge-graph departments.
    result = chordian.Memory.list_departments()
    departments = result.get("departments", [])
    print(f"You have {len(departments)} departments:")
    for dept in departments:
        print(f"  - {dept.get('name')} ({dept.get('graph_id')}): "
              f"{dept.get('node_count')} nodes / {dept.get('edge_count')} edges")

    # Inspect one department in detail.
    if departments:
        graph_id = departments[0]["graph_id"]
        detail = chordian.Memory.get_department(graph_id)
        print(f"\nDepartment {graph_id}: status={detail.get('status')}")

    # Ingest content from Enterprise Search connectors into a graph.
    # `source_types` is required: pass None to ingest all sources, or a list of
    # connector source types (e.g. ["google_drive", "notion"]).
    list_id = sys.argv[1] if len(sys.argv) > 1 else None
    if list_id:
        job = chordian.Memory.ingest_connectors(
            list_id=list_id,
            source_types=None,
            mode="incremental",
        )
        print(f"\nConnector ingestion job: {job.get('jobId')} ({job.get('status')})")


if __name__ == "__main__":
    main()
