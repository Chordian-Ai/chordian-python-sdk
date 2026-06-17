"""Memory: generate a knowledge graph from structured records.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/memory/generate_memory.py <list_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    list_id = sys.argv[1] if len(sys.argv) > 1 else "your-list-id"

    columns = [
        {"id": "company", "header": "Company", "type": "text"},
        {"id": "industry", "header": "Industry", "type": "text"},
    ]
    records = [
        {
            "cells": {"company": "Acme Corp", "industry": "Manufacturing"},
            "step_source": "import",
            "metadata": {"source": "crm"},
        },
        {
            "cells": {"company": "Globex", "industry": "Logistics"},
            "step_source": "import",
            "metadata": {"source": "crm"},
        },
    ]

    job = chordian.Memory.generate(
        list_id=list_id,
        records=records,
        columns=columns,
        workflow_category="company",
    )
    print(f"Generate job: {job.get('jobId')} ({job.get('status')})")


if __name__ == "__main__":
    main()
