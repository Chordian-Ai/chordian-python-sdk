"""EnterpriseSearch.create_chat_session — create a new chat session.

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/create_chat_session.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.EnterpriseSearch.create_chat_session(persona_id=0)
print(response)
