"""CompanySearch.get_search_result — fetch a completed workflow's results.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/get_search_result.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.CompanySearch.get_search_result(thread_id)
print(response)
