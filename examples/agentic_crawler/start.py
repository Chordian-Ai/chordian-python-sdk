"""AgenticCrawler.start — start an agentic crawler workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/agentic_crawler/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `start` blocks server-side until the workflow responds

response = chordian.AgenticCrawler.start(
    prompt="Find US emerging beauty brands with 8M-35M in revenue",
)

print("\nWorkflow started\n")
for label, key in (
    ("Success", "success"),
    ("Status", "status"),
    ("Thread ID", "thread_id"),
    ("List ID", "list_id"),
    ("Workspace ID", "workspace_id"),
    ("Live URL", "live_url"),
    ("WebSocket URL", "websocket_url"),
    ("Message", "message"),
):
    if key in response and response[key] is not None:
        print(f"  {label + ':':<18}{response[key]}")
print()
