"""Enterprise Search: upload a project file and poll its processing status.

Run with:
    export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
    python examples/enterprise_search/upload_file.py path/to/document.pdf
"""

import os
import sys
import time

import chordian

chordian.api_key = os.environ["CHORDIAN_API_KEY"]


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "document.pdf"

    # `files` accepts a path, a list of paths, or (filename, content) tuples.
    result = chordian.EnterpriseSearch.upload_file(path)
    uploaded = result.get("user_files", [])
    rejected = result.get("rejected_files", [])
    print(f"Uploaded {len(uploaded)} file(s); {len(rejected)} rejected.")

    file_ids = [f["id"] for f in uploaded]
    if not file_ids:
        return

    # Poll until all files finish processing.
    for _ in range(20):
        statuses = chordian.EnterpriseSearch.get_file_statuses(file_ids)
        states = {f["id"]: f.get("status") for f in statuses}
        print("  statuses:", states)
        if all(s == "COMPLETED" for s in states.values()):
            print("All files processed.")
            break
        time.sleep(3)


if __name__ == "__main__":
    main()
