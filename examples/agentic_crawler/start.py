"""Start an agentic crawler workflow."""

import chordian

chordian.api_key = "on_tenant_12345.xxxxxxxx"

job = chordian.AgenticCrawler.start(
    prompt="Find US emerging beauty brands with 8M-35M in revenue",
)
print(job["thread_id"])
print(job["websocket_url"])
