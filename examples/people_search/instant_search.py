"""People Search: instant lookup against the existing people index.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/people_search/instant_search.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    response = chordian.PeopleSearch.search(
        query="Jane Doe",
        limit=5,
        path=["fullName", "emails.email"],
        fuzzy_max_edits=1,
    )
    print(f"Found {response.get('count', 0)} people:")
    for person in response.get("results", []):
        emails = ", ".join(person.get("recommended_email", []))
        print(f"  - {person.get('fullName')}  <{emails}>")


if __name__ == "__main__":
    main()
