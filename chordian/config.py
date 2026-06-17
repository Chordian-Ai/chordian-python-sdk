"""Default configuration for the Chordian SDK.

Chordian is served by two backends that share a single API key:

* ``core``   – Company Search, People Search, Deep Research and Enterprise Search.
* ``memory`` – Memory / Knowledge Graph endpoints (a different base URL).

These values are the module-level defaults. They can be overridden at runtime by
setting ``chordian.core_base_url`` / ``chordian.memory_base_url`` (useful for
pointing the SDK at a staging environment), or via the ``CHORDIAN_CORE_BASE_URL``
and ``CHORDIAN_MEMORY_BASE_URL`` environment variables.
"""

import os

CORE_BASE_URL: str = os.environ.get(
    "CHORDIAN_CORE_BASE_URL", "https://chordian-core.chordian.ai"
)
"""Base URL for the Chordian core platform (search, research, enterprise search)."""

MEMORY_BASE_URL: str = os.environ.get(
    "CHORDIAN_MEMORY_BASE_URL", "https://graph-kb.chordian.ai"
)
"""Base URL for the Chordian memory / knowledge-graph service."""

DEFAULT_TIMEOUT: float = 30.0
"""Default per-request timeout, in seconds."""
