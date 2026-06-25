"""Start a Chordian deep search workflow."""

import chordian

chordian.api_key = "on_tenant_12345.xxxxxxxx"

job = chordian.ChordianDeepSearch.start(
    prompt="find Kerala recent startups on ai",
    llm_model="claude-sonnet-4.6",
    live_url=True,
    proxy=False,
)
print(job["thread_id"])
print(job["websocket_url"])
