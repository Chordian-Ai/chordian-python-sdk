# Examples

Runnable scripts for every Chordian API group. Each script reads your API key from
the `CHORDIAN_API_KEY` environment variable.

```bash
pip install chordian
export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
python examples/company_search/start_and_poll.py
```

| Group | Script | What it shows |
|-------|--------|---------------|
| Company Search | [`start_and_poll.py`](company_search/start_and_poll.py) | Start a workflow, poll status, read results |
| Company Search | [`instant_search.py`](company_search/instant_search.py) | Instant index lookup (`/search`) |
| Company Search | [`enrich.py`](company_search/enrich.py) | Enrich a result column |
| People Search | [`start_and_poll.py`](people_search/start_and_poll.py) | Start a workflow and poll |
| People Search | [`instant_search.py`](people_search/instant_search.py) | Instant index lookup |
| Deep Research | [`deep_research_stream.py`](research/deep_research_stream.py) | Start research, stream SSE progress, get the report |
| Deep Research | [`respond_to_clarification.py`](research/respond_to_clarification.py) | Answer a clarifying question mid-stream |
| Enterprise Search | [`chat.py`](enterprise_search/chat.py) | Create a session, stream + non-stream chat |
| Enterprise Search | [`connectors.py`](enterprise_search/connectors.py) | Inspect connectors, trigger indexing |
| Enterprise Search | [`upload_file.py`](enterprise_search/upload_file.py) | Upload a file, poll processing status |
| Memory | [`departments_and_chat.py`](memory/departments_and_chat.py) | Create a graph, upload data, chat |
| Memory | [`generate_memory.py`](memory/generate_memory.py) | Build a graph from structured records |

> Deep Research also needs a service ID — set `CHORDIAN_SERVICE_ID` or pass
> `service_id=...`.
