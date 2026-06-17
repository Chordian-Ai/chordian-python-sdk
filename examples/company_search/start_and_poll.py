"""Company Search: start a workflow, poll until it finishes, read the results.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/start_and_poll.py
"""

import os
import time

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    started = chordian.CompanySearch.start(
        prompt="B2B SaaS companies in Europe focused on developer tools",
        list_name="EU Dev Tools",
        search_mode="fast",
    )
    thread_id = started["thread_id"]
    print(f"Started company search: thread_id={thread_id}")

    # Poll the workflow status until it is no longer running.
    while True:
        status = chordian.CompanySearch.status(thread_id)
        state = status.get("status") or status.get("current_step")
        print(f"  status: {state}")
        if state in {"completed", "done", "finished", "stopped", "error"}:
            break
        time.sleep(3)

    # Fetch the full result table.
    result = chordian.CompanySearch.get_search_result(thread_id)
    companies = result.get("results", [])
    print(f"\nCollected {len(companies)} companies:")
    for company in companies[:10]:
        print(f"  - {company.get('companyName') or company.get('name')}")


if __name__ == "__main__":
    main()
