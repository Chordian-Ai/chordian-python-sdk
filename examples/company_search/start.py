"""CompanySearch.start — start a company search workflow.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/start.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = 300  # `start` blocks server-side until the workflow responds

response = chordian.CompanySearch.start(
    prompt="B2B SaaS companies in Europe focused on developer tools",
    list_name="EU Dev Tools",
    search_mode="fast",
)
print(response)
