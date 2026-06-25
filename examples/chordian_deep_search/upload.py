"""Upload a file into a Chordian deep search workspace."""

import chordian

chordian.api_key = "on_tenant_12345.xxxxxxxx"

result = chordian.ChordianDeepSearch.upload(
    "document.md",
    thread_id="dcb3c14b-4c71-4e26-87d5-d46646c8dc80",
)
print(result["workspace_id"])
print(result["paths"])
