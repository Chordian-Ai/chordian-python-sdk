"""People Search: continue a workflow, enrich a column, then stop.

Covers the remaining People Search endpoints: continue_, start_enrichment,
stop_enrichment and stop.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/enrich_and_manage.py <thread_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    thread_id = sys.argv[1] if len(sys.argv) > 1 else "your-thread-id"

    # Grow the workflow's target.
    chordian.PeopleSearch.continue_(thread_id, total_target=100)
    print(f"Continued {thread_id} to a target of 100.")

    # Enrich a column (people enrichment takes thread_id + column_name).
    chordian.PeopleSearch.start_enrichment(thread_id, column_name="email")
    print("Started enrichment of the 'email' column.")

    # Stop enrichment and the workflow when finished.
    chordian.PeopleSearch.stop_enrichment(thread_id)
    chordian.PeopleSearch.stop(thread_id)
    print("Stopped enrichment and the workflow.")


if __name__ == "__main__":
    main()
