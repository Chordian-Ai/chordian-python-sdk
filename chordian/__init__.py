"""Chordian — the official Python SDK for the Chordian AI platform.

Configure once, then call any resource::

    import chordian

    chordian.api_key = "on_tenant_12345.xxxxxxxx"

    job = chordian.CompanySearch.start(prompt="AI startups in Berlin")
    print(job["thread_id"])

The API key may also be supplied via the ``CHORDIAN_API_KEY`` environment
variable. The same key works for both the core platform and the memory service.
"""

from typing import Optional

from . import config
from ._sse import SSEEvent
from .company_search import CompanySearch
from .enterprise_search import EnterpriseSearch
from .exceptions import (
    ApiError,
    AuthenticationError,
    ChordianError,
    NoApiKeyError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .memory import Memory
from .people_search import PeopleSearch
from .research import Research
from .version import __version__

# ---------------------------------------------------------------------------
# Module-level configuration. Assign to these after importing the package.
# ---------------------------------------------------------------------------

api_key: Optional[str] = None
"""Your Chordian API key (format ``on_tenant_<id>.<token>``).

Falls back to the ``CHORDIAN_API_KEY`` environment variable when left ``None``.
"""

service_id: Optional[str] = None
"""Optional default service ID used for credit tracking / rate limiting.

Endpoints that require a service ID (e.g. Deep Research) use this when a
``service_id`` argument is not passed explicitly.
"""

core_base_url: str = config.CORE_BASE_URL
"""Base URL for the core platform (search, research, enterprise search)."""

memory_base_url: str = config.MEMORY_BASE_URL
"""Base URL for the memory / knowledge-graph service."""

timeout: float = config.DEFAULT_TIMEOUT
"""Per-request timeout, in seconds."""

__all__ = [
    "__version__",
    "api_key",
    "service_id",
    "core_base_url",
    "memory_base_url",
    "timeout",
    # Resources
    "CompanySearch",
    "PeopleSearch",
    "Research",
    "EnterpriseSearch",
    "Memory",
    # Streaming
    "SSEEvent",
    # Exceptions
    "ChordianError",
    "NoApiKeyError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "ApiError",
]
