"""EnterpriseSearch.get_file_statuses — poll processing status for files.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/get_file_statuses.py <file_id> [file_id ...]
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

file_ids = sys.argv[1:] or ["your-file-id"]

response = chordian.EnterpriseSearch.get_file_statuses(file_ids)
print(response)
