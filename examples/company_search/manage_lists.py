"""Company Search: manage lists and workflows.

Covers the remaining Company Search endpoints: get_lists, continue_, stop and
stop_enrichment.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/manage_lists.py [thread_id]
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    # List every saved list for the tenant.
    lists = chordian.CompanySearch.get_lists()
    print(f"You have {lists.get('total', 0)} lists:")
    for item in lists.get("data", []):
        print(f"  - {item.get('listName')} ({item.get('noOfRecords')} records)")

    thread_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not thread_id:
        print("\nPass a thread_id to demo continue_/stop. Skipping.")
        return

    # Grow an existing workflow to a larger target.
    chordian.CompanySearch.continue_(thread_id, total_target=200)
    print(f"Continued {thread_id} to a target of 200.")

    # Stop the workflow (and any running enrichment) when you're done.
    chordian.CompanySearch.stop_enrichment(thread_id)
    chordian.CompanySearch.stop(thread_id)
    print("Stopped the workflow and enrichment.")


if __name__ == "__main__":
    main()
