"""ChordianDeepSearch.start — start a deep search workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/chordian_deep_search/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `start` blocks server-side until the workflow responds

response = chordian.ChordianDeepSearch.start(
    prompt="find Kerala recent startups on ai",
    llm_model="claude-sonnet-4.6",
    live_url=True,
    proxy=False,
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
