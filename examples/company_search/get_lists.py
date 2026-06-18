"""CompanySearch.get_lists — list saved lists for the tenant.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/get_lists.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.CompanySearch.get_lists()
print(response)
