"""EnterpriseSearch.connector_run_once — trigger a one-time reindex.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/connector_run_once.py <connector_id> <credential_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

connector_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
credential_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0

response = chordian.EnterpriseSearch.connector_run_once(
    connector_id=connector_id,
    credential_ids=[credential_id],
    from_beginning=False,
)
print(response)
