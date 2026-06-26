"""WebAndResearch.start — start a web and research workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/webandreasearch/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `start` blocks server-side until the workflow responds

response = chordian.WebAndResearch.start(
    prompt="Research top fintech startups in India",
    live_url=False,
    proxy=False,
    llm_model="chordian-r1",
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
