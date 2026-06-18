"""EnterpriseSearch.get_connectors — list connectors (optional credential filter).

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/get_connectors.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.EnterpriseSearch.get_connectors()
print(response)
