"""Shared pytest fixtures.

All tests run fully offline: ``respx`` intercepts every ``httpx`` request, so no
real network calls are made.
"""

import httpx
import pytest

import chordian
from chordian import _client

CORE = "https://chordian-core.chordian.ai"
MEMORY = "https://graph-kb.chordian.ai"
TEST_KEY = "on_tenant_99999.testtoken"


@pytest.fixture(autouse=True)
def _reset_sdk_state(monkeypatch):
    """Give every test a clean, configured SDK and a fresh shared HTTP client."""
    monkeypatch.delenv("CHORDIAN_API_KEY", raising=False)
    monkeypatch.delenv("CHORDIAN_CORE_BASE_URL", raising=False)
    monkeypatch.delenv("CHORDIAN_MEMORY_BASE_URL", raising=False)

    chordian.api_key = TEST_KEY
    chordian.service_id = None
    chordian.core_base_url = CORE
    chordian.memory_base_url = MEMORY
    chordian.timeout = 30.0

    # Force a fresh client so respx (patched per-test) intercepts it.
    _client.set_http_client(httpx.Client())
    yield
    _client._http_client = None
