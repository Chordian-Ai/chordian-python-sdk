"""Company Search: instant lookup against the existing company index.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/company_search/instant_search.py
"""

import os

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    response = chordian.CompanySearch.search(
        query="stripe.com",
        limit=5,
        path=["website", "companyName"],
        fuzzy_max_edits=1,
    )
    print(f"Found {response.get('count', 0)} companies:")
    for company in response.get("results", []):
        print(f"  - {company.get('companyName')}  ({company.get('website')})")


if __name__ == "__main__":
    main()
