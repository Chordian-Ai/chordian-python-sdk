"""Research.status — get a research workflow's current status.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/research/status.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.Research.status(thread_id)
print(response)
