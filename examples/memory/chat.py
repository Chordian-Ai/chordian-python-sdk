"""Memory.chat — ask a question against a knowledge graph.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/chat.py <list_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

list_id = sys.argv[1] if len(sys.argv) > 1 else "your-graph-id"

response = chordian.Memory.chat(
    list_id=list_id,
    question="What are our key architecture decisions?",
)
print(response)
