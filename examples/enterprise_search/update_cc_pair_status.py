"""EnterpriseSearch.update_cc_pair_status — pause/schedule a CC pair.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/update_cc_pair_status.py <cc_pair_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

cc_pair_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# status: SCHEDULED | INITIAL_INDEXING | ACTIVE | PAUSED | DELETING | INVALID
response = chordian.EnterpriseSearch.update_cc_pair_status(cc_pair_id, status="PAUSED")
print(response)
