"""EnterpriseSearch.get_chat_sessions — list the user's chat sessions.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/get_chat_sessions.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.EnterpriseSearch.get_chat_sessions()
print(response)
