"""Memory.get_department — fetch a single department by graph_id.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/get_department.py <graph_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

graph_id = sys.argv[1] if len(sys.argv) > 1 else "your-graph-id"

response = chordian.Memory.get_department(graph_id)
print(response)
