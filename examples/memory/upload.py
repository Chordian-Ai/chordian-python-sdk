"""Memory.upload — upload a file to ingest into a graph.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/upload.py <list_id> <path/to/file>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

list_id = sys.argv[1] if len(sys.argv) > 1 else "your-graph-id"
path = sys.argv[2] if len(sys.argv) > 2 else "notes.txt"

response = chordian.Memory.upload(file=path, list_id=list_id)
print(response)
