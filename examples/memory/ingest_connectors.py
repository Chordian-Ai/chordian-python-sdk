"""Memory.ingest_connectors — ingest connector content into a graph.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/ingest_connectors.py <list_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

list_id = sys.argv[1] if len(sys.argv) > 1 else "your-graph-id"

# source_types is required: None ingests all sources, or pass e.g. ["google_drive"].
response = chordian.Memory.ingest_connectors(
    list_id=list_id,
    source_types=None,
    mode="incremental",
)
print(response)
