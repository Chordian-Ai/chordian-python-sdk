"""Memory.list_departments — list knowledge-graph departments.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/list_departments.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.Memory.list_departments()
print(response)
