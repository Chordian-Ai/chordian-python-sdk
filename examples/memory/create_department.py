"""Memory.create_department — create a new knowledge-graph department.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/create_department.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.Memory.create_department(
    name="Engineering Knowledge",
    description="Architecture decisions and runbooks",
    source_type="department",
)
print(response)
