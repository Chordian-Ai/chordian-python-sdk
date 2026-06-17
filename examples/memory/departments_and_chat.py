"""Memory: create a department, upload a file, then chat with the graph.

The Memory API is served by the memory service (a different base URL); the SDK
routes there automatically using the same API key.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/departments_and_chat.py path/to/notes.txt
"""

import os
import sys
import time

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "notes.txt"

    # 1. Create a department (a knowledge graph).
    dept = chordian.Memory.create_department(
        name="Engineering Knowledge",
        description="Architecture decisions and runbooks",
        source_type="upload",
    )
    list_id = dept.get("list_id") or dept.get("graph_id")
    print(f"Created department: graph_id={dept.get('graph_id')} list_id={list_id}")

    # 2. Upload a file to ingest into the graph.
    job = chordian.Memory.upload(file=path, list_id=list_id)
    print(f"Upload job: {job.get('jobId')} ({job.get('status')})")

    # Give ingestion a moment (real apps should poll a job-status endpoint).
    time.sleep(5)

    # 3. Ask a question against the graph.
    answer = chordian.Memory.chat(
        list_id=list_id,
        question="What are our key architecture decisions?",
    )
    print("\nAnswer:", answer.get("answer"))
    print(f"(graph: {len(answer.get('nodes', []))} nodes, "
          f"{len(answer.get('edges', []))} edges)")


if __name__ == "__main__":
    main()
