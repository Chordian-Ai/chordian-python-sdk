"""Lightweight client-side request validation for the Chordian SDK.

These checks catch obvious mistakes before a network round-trip. The server
remains the source of truth for full schema validation (e.g. country codes).
"""

from typing import Optional


def require_non_empty_prompt(prompt: str) -> str:
    """Return ``prompt`` stripped; raise if missing or whitespace-only."""
    if not isinstance(prompt, str):
        raise ValueError("prompt must be a string")
    stripped = prompt.strip()
    if not stripped:
        raise ValueError("prompt must not be empty")
    return stripped


def normalize_optional_str(value: Optional[str]) -> Optional[str]:
    """Treat empty strings as ``None`` for optional id fields."""
    if value is None or value == "":
        return None
    return value


def validate_proxy_settings(
    *,
    proxy: bool,
    live_url: Optional[bool] = None,
    proxy_country_code: Optional[str] = None,
    require_live_url_when_proxy: bool = False,
) -> Optional[str]:
    """Validate proxy-related fields; return normalized ``proxy_country_code``."""
    code = normalize_optional_str(proxy_country_code)
    if proxy:
        if require_live_url_when_proxy and live_url is False:
            raise ValueError("live_url must be true when proxy is true")
        if not code:
            raise ValueError("proxy_country_code is required when proxy is true")
        return code.lower()
    return code.lower() if code else None
