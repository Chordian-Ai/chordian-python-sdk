"""Deep Research: list active workflows and stop one.

Covers the remaining Deep Research endpoints: active and stop.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/research/active_and_stop.py [thread_id]
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    active = chordian.Research.active()
    print("Active research workflows:", active)

    thread_id = sys.argv[1] if len(sys.argv) > 1 else None
    if thread_id:
        result = chordian.Research.stop(thread_id)
        print(f"Stopped {thread_id}:", result)


if __name__ == "__main__":
    main()
