"""EnterpriseSearch.rename_chat_session — rename a chat session.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/rename_chat_session.py <chat_session_id>
"""

import os
import sys

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

chat_session_id = sys.argv[1] if len(sys.argv) > 1 else "your-chat-session-id"

response = chordian.EnterpriseSearch.rename_chat_session(chat_session_id, name="Q3 Analysis")
print(response)
