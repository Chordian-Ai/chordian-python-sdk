"""Enterprise Search: create a chat session and stream an answer.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/chat.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    session = chordian.EnterpriseSearch.create_chat_session(persona_id=0)
    chat_session_id = session["chat_session_id"]
    print(f"Created chat session: {chat_session_id}\n")

    # Streaming answer (Server-Sent Events).
    print("Streaming answer:")
    for event in chordian.EnterpriseSearch.send_chat_message(
        message="Summarise our Q3 sales performance.",
        chat_session_id=chat_session_id,
        stream=True,
        include_citations=True,
    ):
        print(f"  [{event.event}] {event.json if event.json is not None else event.data}")

    # Non-streaming answer (single JSON response).
    answer = chordian.EnterpriseSearch.send_chat_message(
        message="And how does that compare to Q2?",
        chat_session_id=chat_session_id,
        stream=False,
    )
    print("\nFull response keys:", list(answer.keys()))


if __name__ == "__main__":
    main()
