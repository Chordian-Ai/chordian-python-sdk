"""Research.start — start a deep research workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    export CHORDIAN_SERVICE_ID="your-service-id"
    python examples/research/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.service_id = os.environ.get("CHORDIAN_SERVICE_ID")

response = chordian.Research.start(
    query="Analyze the competitive landscape of AI coding assistants",
    allow_clarification=True,
)
print(response)
