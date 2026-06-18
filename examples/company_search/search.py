"""CompanySearch.search — instant lookup against the company index.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/search.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.CompanySearch.search(
    query="amossoftware.com",
    limit=10,
    path=["website", "companyName"],
    fuzzy_max_edits=2,
)
print(response)
