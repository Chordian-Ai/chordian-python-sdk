"""Deep Research: start a research run and stream progress to completion.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    export CHORDIAN_SERVICE_ID="your-service-id"
    python examples/research/deep_research_stream.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.service_id = os.environ.get("CHORDIAN_SERVICE_ID")


def main() -> None:
    started = chordian.Research.start(
        query="What are the leading approaches to retrieval-augmented generation in 2026?",
        allow_clarification=False,
        max_concurrent_research_units=4,
    )
    thread_id = started["thread_id"]
    print(f"Started research: thread_id={thread_id}\n")

    final_report = None
    for event in chordian.Research.stream(thread_id):
        payload = event.json
        print(f"[{event.event}] {payload if payload is not None else event.data}")
        if event.event in {"complete", "completed", "done"} and isinstance(payload, dict):
            final_report = payload.get("final_report")

    if final_report:
        print("\n===== FINAL REPORT =====\n")
        print(final_report)
    else:
        # Fall back to a status poll if the report wasn't on the stream.
        status = chordian.Research.status(thread_id)
        print("\nFinal status:", status.get("status"))
        if status.get("final_report"):
            print(status["final_report"])


if __name__ == "__main__":
    main()
