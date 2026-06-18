"""Minimal Server-Sent Events (SSE) parser.

Chordian streams workflow progress (Deep Research, Enterprise chat) as SSE. This
module turns a stream of raw text lines into a sequence of :class:`SSEEvent`
objects following the `WHATWG SSE specification
<https://html.spec.whatwg.org/multipage/server-sent-events.html>`_ (the subset we
need: ``event``, ``data`` and ``id`` fields, blank line dispatches the event).
"""

import json
from typing import Any, Iterable, Iterator, List, NamedTuple, Optional


class SSEEvent(NamedTuple):
    """A single Server-Sent Event."""

    event: str
    """The event type (the ``event:`` field, or ``"message"`` if absent)."""

    data: str
    """The raw concatenated ``data:`` payload."""

    id: Optional[str] = None
    """The ``id:`` field, if present."""

    @property
    def json(self) -> Any:
        """Parse :attr:`data` as JSON, returning ``None`` if it is not valid JSON."""
        if not self.data:
            return None
        try:
            return json.loads(self.data)
        except (ValueError, TypeError):
            return None


def parse_sse(lines: Iterable[str]) -> Iterator[SSEEvent]:
    """Parse an iterable of decoded text lines into :class:`SSEEvent` objects.

    A blank line dispatches the buffered event. ``data`` fields accumulate across
    multiple lines, joined with ``"\\n"`` per the spec.
    """
    event_type = ""
    data_lines: List[str] = []
    last_id: Optional[str] = None

    for raw in lines:
        line = raw.rstrip("\n").rstrip("\r")

        # Blank line: dispatch the buffered event (if any).
        if line == "":
            if data_lines or event_type:
                yield SSEEvent(
                    event=event_type or "message",
                    data="\n".join(data_lines),
                    id=last_id,
                )
            event_type = ""
            data_lines = []
            continue

        # Comment line.
        if line.startswith(":"):
            continue

        field, _, value = line.partition(":")
        # A leading space after the colon is part of the syntax, not the value.
        if value.startswith(" "):
            value = value[1:]

        if field == "event":
            event_type = value
        elif field == "data":
            data_lines.append(value)
        elif field == "id":
            last_id = value
        # Unknown fields (e.g. "retry") are ignored.

    # Flush a trailing event that was not terminated by a blank line.
    if data_lines or event_type:
        yield SSEEvent(
            event=event_type or "message",
            data="\n".join(data_lines),
            id=last_id,
        )
