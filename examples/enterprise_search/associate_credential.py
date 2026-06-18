"""EnterpriseSearch.associate_credential — link a credential to a connector.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/associate_credential.py <connector_id> <credential_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

connector_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
credential_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0

response = chordian.EnterpriseSearch.associate_credential(
    connector_id=connector_id,
    credential_id=credential_id,
    name="Docs creds",
    access_type="public",
)
print(response)
