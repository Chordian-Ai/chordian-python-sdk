"""Start a web and research search workflow."""

import chordian

chordian.api_key = "on_tenant_12345.xxxxxxxx"

job = chordian.WebAndResearch.start(
    prompt="Research top fintech startups in India",
    live_url=False,
    proxy=False,
    llm_model="chordian-r1",
)
print(job["thread_id"])
print(job["websocket_url"])
