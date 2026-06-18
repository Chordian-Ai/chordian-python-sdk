# Chordian Python SDK

[![PyPI version](https://img.shields.io/pypi/v/chordian.svg)](https://pypi.org/project/chordian/)
[![Python versions](https://img.shields.io/pypi/pyversions/chordian.svg)](https://pypi.org/project/chordian/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The official Python SDK for the [Chordian](https://chordian.ai) AI platform. It wraps every
API available with your API key:

- **Company Search** — find and enrich companies from natural-language prompts
- **People Search** — find and enrich people from natural-language prompts
- **Deep Research** — multi-agent research workflows with live streaming
- **Enterprise Search** — chat over your indexed knowledge, manage connectors, upload files
- **Memory** — build knowledge graphs and chat with them

A single API key works across both Chordian backends (the core platform and the memory
service); the SDK routes each call to the right base URL automatically.

## Installation

```bash
pip install chordian
```

Requires Python 3.8+.

## Quickstart

```python
import chordian

chordian.api_key = "on_tenant_12345.xxxxxxxx"  # or set CHORDIAN_API_KEY in the environment

# Start a company search, then read the results.
job = chordian.CompanySearch.start(prompt="AI startups in Berlin", search_mode="fast")
print(job["thread_id"])
```

The API key may also be supplied via the `CHORDIAN_API_KEY` environment variable, in which
case you don't need to set `chordian.api_key` at all.

## Authentication

Your key has the format `on_tenant_<id>.<token>` and is sent as
`Authorization: Bearer <key>`. Configure it once:

```python
import chordian
chordian.api_key = "on_tenant_12345.xxxxxxxx"
```

```bash
# or, via environment variable
export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
```

## Usage by API

### Company Search

```python
# Asynchronous workflow: start → poll → read results
started = chordian.CompanySearch.start(prompt="B2B SaaS in Europe", list_name="EU SaaS")
thread_id = started["thread_id"]

status = chordian.CompanySearch.status(thread_id)         # poll progress
result = chordian.CompanySearch.get_search_result(thread_id)

# Collect more, or enrich a column
chordian.CompanySearch.continue_(thread_id, total_target=200)
chordian.CompanySearch.start_enrichment(thread_id, column_name="Funding",
                                        instruction="latest funding round")

# Instant lookup against the index
hits = chordian.CompanySearch.search(query="stripe.com", limit=5, path=["website"])
```

### People Search

```python
started = chordian.PeopleSearch.start(prompt="VP Eng at Series B fintechs")
status = chordian.PeopleSearch.status(started["thread_id"])
hits = chordian.PeopleSearch.search(query="Jane Doe", limit=5, path=["fullName"])
```

### Deep Research (streaming)

```python
chordian.service_id = "your-service-id"   # required for research

run = chordian.Research.start(query="State of RAG in 2026", allow_clarification=False)
for event in chordian.Research.stream(run["thread_id"]):
    print(event.event, event.json)        # SSE: progress, clarification, complete, ...

final = chordian.Research.status(run["thread_id"])
print(final.get("final_report"))
```

### Enterprise Search

```python
session = chordian.EnterpriseSearch.create_chat_session()
sid = session["chat_session_id"]

# Stream an answer
for event in chordian.EnterpriseSearch.send_chat_message(
    message="Summarise Q3 sales", chat_session_id=sid, stream=True, include_citations=True
):
    print(event.json)

# Or get one JSON response
answer = chordian.EnterpriseSearch.send_chat_message(message="Compare to Q2", chat_session_id=sid)

# Connectors & files
chordian.EnterpriseSearch.get_connector_status()
chordian.EnterpriseSearch.upload_file("report.pdf")
```

### Memory (Knowledge Graph)

```python
dept = chordian.Memory.create_department(name="Engineering Knowledge")
list_id = dept["list_id"]

chordian.Memory.upload(file="runbook.md", list_id=list_id)
answer = chordian.Memory.chat(list_id=list_id, question="What are our key decisions?")
print(answer["answer"], answer["nodes"], answer["edges"])
```

## Streaming

Deep Research and Enterprise chat support Server-Sent Events. Streaming methods return an
iterator of `chordian.SSEEvent` objects:

```python
for event in chordian.Research.stream(thread_id):
    print(event.event)   # event type, e.g. "progress", "complete"
    print(event.data)    # raw data string
    print(event.json)    # parsed JSON payload (or None if not JSON)
```

## Configuration

| Setting | Default | Purpose |
|---------|---------|---------|
| `chordian.api_key` | `CHORDIAN_API_KEY` env | Your API key |
| `chordian.service_id` | `None` | Default service ID (required by Deep Research) |
| `chordian.core_base_url` | `https://chordian-core.chordian.ai` | Core platform base URL |
| `chordian.memory_base_url` | `https://graph-kb.chordian.ai` | Memory service base URL |
| `chordian.timeout` | `30.0` | Per-request timeout (seconds) |

Base URLs can also be overridden with the `CHORDIAN_CORE_BASE_URL` and
`CHORDIAN_MEMORY_BASE_URL` environment variables (handy for staging).

## Error handling

Every error subclasses `chordian.ChordianError`:

```python
from chordian import ChordianError, AuthenticationError, RateLimitError

try:
    chordian.CompanySearch.start(prompt="...")
except AuthenticationError:
    ...  # 401 — bad/missing key
except RateLimitError:
    ...  # 429 — slow down
except ChordianError as e:
    print(e.status_code, e.message)
```

Other subclasses: `NoApiKeyError`, `PermissionDeniedError`, `NotFoundError`,
`ValidationError`, `ServerError`, `APITimeoutError`, `APIConnectionError`, `ApiError`.

### Timeouts and long-running endpoints

`chordian.timeout` defaults to 30 seconds. Some endpoints respond synchronously and
block until their work finishes — notably `CompanySearch.start` / `continue_` and
`PeopleSearch.start` / `continue_`. For those, raise the timeout; for streaming
(`Research.stream`, `send_chat_message(stream=True)`), disable it:

```python
chordian.timeout = 300    # seconds, for long-running start/continue calls
chordian.timeout = None   # no timeout, for SSE streaming
```

A timeout raises `chordian.APITimeoutError`; an unreachable host raises
`chordian.APIConnectionError`.

## Examples

Runnable scripts for every API live in [`examples/`](examples/). See
[examples/README.md](examples/README.md).

## Development

```bash
git clone https://github.com/chordian-ai/chordian-python.git
cd chordian-python
pip install -e ".[dev]"

pytest            # run the (offline) test suite
ruff check .      # lint
mypy chordian     # type-check
```

## License

[MIT](LICENSE)
