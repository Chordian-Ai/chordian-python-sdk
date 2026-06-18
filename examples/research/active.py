"""Research.active — list active research workflows.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/research/active.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.Research.active()
print(response)
