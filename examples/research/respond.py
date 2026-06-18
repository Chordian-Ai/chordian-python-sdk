"""Research.respond — answer a clarifying question and resume research.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/research/respond.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.Research.respond(
    thread_id,
    response="Focus on code completion accuracy.",
)
print(response)
