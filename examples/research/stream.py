"""Research.stream — stream a research workflow's progress (SSE).

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/research/stream.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = None  # SSE stream: disable the read timeout

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

for event in chordian.Research.stream(thread_id):
    print(event.event, event.json if event.json is not None else event.data)
