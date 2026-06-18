"""PeopleSearch.start — start a people search workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `start` blocks server-side until the workflow responds

response = chordian.PeopleSearch.start(
    prompt="VP-level engineering leaders at Series B fintech companies in the US",
    list_name="Fintech Eng Leaders",
    search_mode="fast",
)
print(response)
