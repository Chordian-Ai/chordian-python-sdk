"""PeopleSearch.start_enrichment — enrich a column on a workflow's table.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/start_enrichment.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.PeopleSearch.start_enrichment(thread_id, column_name="email")
print(response)
