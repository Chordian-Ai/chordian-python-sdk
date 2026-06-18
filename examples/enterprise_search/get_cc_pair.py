"""EnterpriseSearch.get_cc_pair — full info for a connector-credential pair.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/get_cc_pair.py <cc_pair_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

cc_pair_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0

response = chordian.EnterpriseSearch.get_cc_pair(cc_pair_id)
print(response)
