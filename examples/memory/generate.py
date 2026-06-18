"""Memory.generate — build a graph from structured records.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/generate.py <list_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

list_id = sys.argv[1] if len(sys.argv) > 1 else "your-list-id"

response = chordian.Memory.generate(
    list_id=list_id,
    records=[
        {
            "cells": {"company": "Acme Corp", "industry": "Manufacturing"},
            "step_source": "import",
            "metadata": {"source": "crm"},
        }
    ],
    columns=[
        {"id": "company", "header": "Company", "type": "fixed"},
        {"id": "industry", "header": "Industry", "type": "dynamic"},
    ],
    workflow_category="company",
)
print(response)
