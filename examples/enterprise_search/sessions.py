"""Enterprise Search: manage chat sessions.

Covers create_chat_session, get_chat_sessions and rename_chat_session.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/sessions.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    # Create a session.
    session = chordian.EnterpriseSearch.create_chat_session(persona_id=0)
    sid = session["chat_session_id"]
    print(f"Created session {sid}")

    # Rename it.
    renamed = chordian.EnterpriseSearch.rename_chat_session(sid, name="Q3 Analysis")
    print("Renamed to:", renamed.get("new_name"))

    # List all sessions for the user.
    sessions = chordian.EnterpriseSearch.get_chat_sessions()
    print(f"You have {len(sessions.get('sessions', []))} sessions:")
    for s in sessions.get("sessions", []):
        print(f"  - {s.get('name')} ({s.get('id')})")


if __name__ == "__main__":
    main()
