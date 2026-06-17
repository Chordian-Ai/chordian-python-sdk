"""People Search: start a workflow and poll until it finishes.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/start_and_poll.py
"""

import os
import time

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    started = chordian.PeopleSearch.start(
        prompt="VP of Engineering at Series B fintech startups in the US",
        list_name="Fintech Eng Leaders",
        search_mode="fast",
    )
    thread_id = started["thread_id"]
    print(f"Started people search: thread_id={thread_id}")

    while True:
        status = chordian.PeopleSearch.status(thread_id)
        state = status.get("status") or status.get("current_step")
        print(f"  status: {state}")
        if state in {"completed", "done", "finished", "stopped", "error"}:
            break
        time.sleep(3)

    table = status.get("table_structure", {})
    rows = table.get("rows", [])
    print(f"\nCollected {len(rows)} people.")


if __name__ == "__main__":
    main()
