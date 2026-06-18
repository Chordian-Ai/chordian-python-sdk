"""PeopleSearch.continue_ — grow an existing workflow's target.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/continue_search.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `continue_` blocks server-side until the workflow responds

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.PeopleSearch.continue_(thread_id, total_target=200)
print(response)
