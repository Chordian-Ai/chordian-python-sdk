"""EnterpriseSearch.get_connector_status — status for all connectors.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/get_connector_status.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.EnterpriseSearch.get_connector_status()
print(response)
