"""EnterpriseSearch.create_connector — create a connector (e.g. web).

    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/create_connector.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]

response = chordian.EnterpriseSearch.create_connector(
    name="Docs site",
    source="web",
    input_type="load_state",
    connector_specific_config={
        "base_url": "https://docs.example.com",
        "web_connector_type": "recursive",
    },
    refresh_freq=86400,
    access_type="public",
)
print(response)
