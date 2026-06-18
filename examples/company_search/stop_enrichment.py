"""CompanySearch.stop_enrichment — stop a running enrichment.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/stop_enrichment.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

response = chordian.CompanySearch.stop_enrichment(thread_id)
print(response)
