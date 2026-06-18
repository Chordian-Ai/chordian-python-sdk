"""EnterpriseSearch.send_chat_message — send a message (streamed via SSE).

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/send_chat_message.py <chat_session_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]
chordian.timeout = None  # SSE stream: disable the read timeout

chat_session_id = sys.argv[1] if len(sys.argv) > 1 else "your-chat-session-id"

for event in chordian.EnterpriseSearch.send_chat_message(
    message="Summarise our Q3 sales performance.",
    chat_session_id=chat_session_id,
    stream=True,
    include_citations=True,
):
    print(event.event, event.json if event.json is not None else event.data)
