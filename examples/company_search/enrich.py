"""Company Search: enrich a column on an existing workflow result table.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/enrich.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

    chordian.CompanySearch.start_enrichment(
        thread_id=thread_id,
        column_name="Funding",
        instruction="Find the company's most recent funding round and amount",
        enrichment_type="custom",
        data_type="company",
    )
    print(f"Enrichment started for thread {thread_id}.")
    print("Poll CompanySearch.status(thread_id) to watch progress, then")
    print("CompanySearch.stop_enrichment(thread_id) to stop early if needed.")


if __name__ == "__main__":
    main()
