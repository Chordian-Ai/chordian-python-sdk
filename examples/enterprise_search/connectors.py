"""Enterprise Search: connector administration.

Covers get_connector_status, get_connectors, get_cc_pair, update_cc_pair_status,
and (commented, since they mutate state) create_connector, connector_run_once,
associate_credential and create_deletion_attempt.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/connectors.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    # List every connector-credential pair and its status.
    statuses = chordian.EnterpriseSearch.get_connector_status()
    print(f"You have {len(statuses)} connector-credential pairs.")
    for pair in statuses:
        print(f"  - cc_pair {pair.get('cc_pair_id')}: {pair.get('name')}")

    # List connectors (optionally filtered by credential ID).
    connectors = chordian.EnterpriseSearch.get_connectors()
    print(f"Total connectors: {len(connectors)}")

    # Inspect a single connector-credential pair, then pause it.
    if statuses:
        cc_pair_id = statuses[0]["cc_pair_id"]
        pair = chordian.EnterpriseSearch.get_cc_pair(cc_pair_id)
        print(f"cc_pair {cc_pair_id} status: {pair.get('status')}, "
              f"docs indexed: {pair.get('num_docs_indexed')}")
        chordian.EnterpriseSearch.update_cc_pair_status(cc_pair_id, status="PAUSED")
        print(f"Paused cc_pair {cc_pair_id}.")

    # The following mutate state and are commented out:
    #
    # connector = chordian.EnterpriseSearch.create_connector(
    #     name="Docs site",
    #     source="web",
    #     input_type="load_state",
    #     connector_specific_config={
    #         "base_url": "https://docs.example.com",
    #         "web_connector_type": "recursive",
    #     },
    #     refresh_freq=86400,
    #     access_type="public",
    # )
    # chordian.EnterpriseSearch.associate_credential(
    #     connector_id=connector["id"], credential_id=0, name="Docs creds"
    # )
    # chordian.EnterpriseSearch.connector_run_once(
    #     connector_id=connector["id"], credential_ids=[0], from_beginning=True
    # )
    # chordian.EnterpriseSearch.create_deletion_attempt(
    #     connector_id=connector["id"], credential_id=0
    # )


if __name__ == "__main__":
    main()
