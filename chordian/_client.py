"""Internal HTTP layer for the Chordian SDK.

Every resource method funnels through :class:`Request`, which resolves the API
key and base URL, builds the ``Authorization`` header, performs the call with
``httpx`` and maps non-2xx responses onto the :mod:`chordian.exceptions` hierarchy.

This module is internal — application code should use the resource classes
(``chordian.CompanySearch`` etc.), not :class:`Request` directly.
"""

import os
from typing import Any, Dict, Iterator, Mapping, Optional

import httpx

from ._sse import SSEEvent, parse_sse
from .exceptions import (
    APIConnectionError,
    APITimeoutError,
    NoApiKeyError,
    error_for_status,
)

# A single shared client gives us connection pooling across calls. It is created
# lazily so that import of the package never opens a socket.
_http_client: Optional[httpx.Client] = None


def _get_http_client() -> httpx.Client:
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client()
    return _http_client


def set_http_client(client: httpx.Client) -> None:
    """Override the shared :class:`httpx.Client` (advanced use / testing)."""
    global _http_client
    _http_client = client


def _resolve_api_key() -> str:
    # Imported lazily to avoid a circular import at package load time.
    import chordian

    key = chordian.api_key or os.environ.get("CHORDIAN_API_KEY")
    if not key:
        raise NoApiKeyError(
            "No API key configured. Set `chordian.api_key = \"...\"` or export the "
            "CHORDIAN_API_KEY environment variable."
        )
    return key


def _resolve_base_url(backend: str) -> str:
    import chordian

    if backend == "memory":
        return chordian.memory_base_url.rstrip("/")
    return chordian.core_base_url.rstrip("/")


def _resolve_timeout() -> Optional[float]:
    import chordian

    return chordian.timeout


def _build_headers(send_json: bool, extra: Optional[Mapping[str, str]]) -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {_resolve_api_key()}",
        "Accept": "application/json",
        "User-Agent": _user_agent(),
    }
    # For multipart uploads we let httpx set Content-Type (it must include the
    # multipart boundary), so we only set it for JSON bodies.
    if send_json:
        headers["Content-Type"] = "application/json"
    if extra:
        headers.update(extra)
    return headers


def _user_agent() -> str:
    import chordian

    return f"chordian-python/{chordian.__version__}"


class Request:
    """A single Chordian API request.

    Parameters
    ----------
    path:
        The endpoint path, e.g. ``"/company-search/start"``.
    verb:
        HTTP method (``"GET"``, ``"POST"``, ``"PUT"``, ``"DELETE"``).
    backend:
        Which base URL to use — ``"core"`` (default) or ``"memory"``.
    json:
        A JSON-serialisable request body.
    params:
        Query-string parameters.
    files:
        ``httpx``-style files mapping for ``multipart/form-data`` uploads. When
        set, ``json`` is ignored and the body is sent as multipart (``data`` may
        carry additional form fields).
    data:
        Extra form fields to accompany a multipart upload.
    """

    def __init__(
        self,
        path: str,
        verb: str,
        *,
        backend: str = "core",
        json: Optional[Any] = None,
        params: Optional[Mapping[str, Any]] = None,
        files: Optional[Any] = None,
        data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.path = path
        self.verb = verb.upper()
        self.backend = backend
        self.json = json
        self.params = _drop_none(params) if params else None
        self.files = files
        self.data = data
        self.headers = headers

    @property
    def url(self) -> str:
        return f"{_resolve_base_url(self.backend)}{self.path}"

    def _request_kwargs(self, *, sending_multipart: bool) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "headers": _build_headers(
                send_json=not sending_multipart and self.json is not None,
                extra=self.headers,
            ),
            "timeout": _resolve_timeout(),
        }
        if self.params:
            kwargs["params"] = self.params
        if sending_multipart:
            if self.files is not None:
                kwargs["files"] = self.files
            if self.data is not None:
                kwargs["data"] = self.data
        elif self.json is not None:
            kwargs["json"] = self.json
        return kwargs

    def perform(self) -> Any:
        """Execute the request and return the parsed JSON response.

        Raises a :class:`~chordian.exceptions.ChordianError` subclass for any
        non-2xx response.
        """
        client = _get_http_client()
        kwargs = self._request_kwargs(sending_multipart=self.files is not None)
        try:
            response = client.request(self.verb, self.url, **kwargs)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(_timeout_message(self.url, kwargs["timeout"])) from exc
        except httpx.TransportError as exc:
            raise APIConnectionError(
                f"Could not connect to {self.url}: {exc}"
            ) from exc
        return _handle_response(response)

    def stream(self) -> Iterator[SSEEvent]:
        """Execute the request and yield Server-Sent Events as they arrive.

        Used for streaming endpoints (Deep Research progress, Enterprise chat).
        """
        client = _get_http_client()
        kwargs = self._request_kwargs(sending_multipart=self.files is not None)
        kwargs["headers"]["Accept"] = "text/event-stream"
        try:
            with client.stream(self.verb, self.url, **kwargs) as response:
                if response.status_code >= 400:
                    response.read()
                    _raise_for_response(response)
                yield from parse_sse(response.iter_lines())
        except httpx.TimeoutException as exc:
            raise APITimeoutError(_timeout_message(self.url, kwargs["timeout"])) from exc
        except httpx.TransportError as exc:
            raise APIConnectionError(f"Could not connect to {self.url}: {exc}") from exc


def _handle_response(response: httpx.Response) -> Any:
    if response.status_code >= 400:
        _raise_for_response(response)
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _format_validation_detail(detail: list) -> str:
    """Turn a FastAPI ``detail`` list into a readable error message."""
    lines = []
    for item in detail:
        if not isinstance(item, dict):
            lines.append(str(item))
            continue
        loc = item.get("loc", ())
        field_parts = [str(part) for part in loc if part != "body"]
        field = ".".join(field_parts) if field_parts else "request"
        msg = item.get("msg", "validation error")
        lines.append(f"{field}: {msg}")
    return "; ".join(lines)


def _raise_for_response(response: httpx.Response) -> None:
    message = f"HTTP {response.status_code}"
    error_type = None
    body: Any = None
    try:
        body = response.json()
        if isinstance(body, dict):
            detail = body.get("detail") or body.get("message") or body.get("error")
            if isinstance(detail, list):
                detail = _format_validation_detail(detail)
            if detail:
                message = str(detail)
            error_type = body.get("type") or body.get("error_type")
    except ValueError:
        if response.text:
            message = response.text
    raise error_for_status(
        response.status_code, message, error_type=error_type, body=body
    )


def _timeout_message(url: str, timeout: Any) -> str:
    return (
        f"Request to {url} timed out after {timeout}s. Long-running endpoints "
        "(e.g. CompanySearch.start) may need a higher timeout — set "
        "`chordian.timeout = 300` (seconds), or `None` to disable it."
    )


def _drop_none(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``mapping`` with ``None`` values removed."""
    return {k: v for k, v in mapping.items() if v is not None}


def build_body(**fields: Any) -> Dict[str, Any]:
    """Build a JSON body, omitting keys whose value is ``None``."""
    return _drop_none(fields)
