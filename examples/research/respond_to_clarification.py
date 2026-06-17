"""Deep Research: handle a clarifying question while streaming.

When ``allow_clarification=True`` the agent may pause to ask a question. This
example answers it and keeps streaming.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    export CHORDIAN_SERVICE_ID="your-service-id"
    python examples/research/respond_to_clarification.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.service_id = os.environ.get("CHORDIAN_SERVICE_ID")


def main() -> None:
    started = chordian.Research.start(
        query="Compare the top project management tools",
        allow_clarification=True,
    )
    thread_id = started["thread_id"]
    print(f"Started research: thread_id={thread_id}\n")

    answered = False
    for event in chordian.Research.stream(thread_id):
        payload = event.json
        print(f"[{event.event}] {payload if payload is not None else event.data}")

        if event.event in {"clarification", "clarify"} and not answered:
            # In a real app, prompt the user. Here we answer programmatically.
            chordian.Research.respond(
                thread_id,
                response="Focus on tools for engineering teams of 10-50 people.",
            )
            answered = True
            print("  -> sent clarification response")


if __name__ == "__main__":
    main()
