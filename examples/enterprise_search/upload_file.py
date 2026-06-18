"""EnterpriseSearch.upload_file — upload a project file for indexing.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/upload_file.py <path/to/file>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

path = sys.argv[1] if len(sys.argv) > 1 else "document.pdf"

response = chordian.EnterpriseSearch.upload_file(path)
print(response)
