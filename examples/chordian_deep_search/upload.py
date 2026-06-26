"""ChordianDeepSearch.upload — upload a file into a deep search workspace.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/chordian_deep_search/upload.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

result = chordian.ChordianDeepSearch.upload(
    "document.md",
    thread_id="dcb3c14b-4c71-4e26-87d5-d46646c8dc80",
)
print(result["workspace_id"])
print(result["paths"])
