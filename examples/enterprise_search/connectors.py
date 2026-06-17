"""Enterprise Search: inspect connectors and trigger a one-off indexing run.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/connectors.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    statuses = chordian.EnterpriseSearch.get_connector_status()
    print(f"You have {len(statuses)} connector-credential pairs.")
    for pair in statuses:
        print(f"  - {pair.get('name')}: {pair.get('status')}")

    # Example: create a simple web connector (commented out to avoid side effects).
    # connector = chordian.EnterpriseSearch.create_connector(
    #     name="Docs site",
    #     source="web",
    #     input_type="load_state",
    #     connector_specific_config={
    #         "base_url": "https://docs.example.com",
    #         "web_connector_type": "recursive",
    #     },
    #     refresh_freq=86400,
    #     access_type="private",
    # )
    # chordian.EnterpriseSearch.connector_run_once(
    #     connector_id=connector["id"], credential_ids=[0], from_beginning=True
    # )


if __name__ == "__main__":
    main()
