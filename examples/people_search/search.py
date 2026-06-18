"""PeopleSearch.search — instant lookup against the people index.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/search.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

# `path` values must be from the API's allowed field enum, e.g. fullName,
# linkedin, email, position, current_employer (NOT dot-notation paths).
response = chordian.PeopleSearch.search(
    query="Jane Smith",
    limit=10,
    path=["fullName", "email"],
    fuzzy_max_edits=2,
)
print(response)
