# Examples

Runnable scripts for every Chordian API group. Each script reads your API key from
the `CHORDIAN_API_KEY` environment variable.

```bash
pip install chordian
export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
python examples/company_search/start_and_poll.py
```

Together these scripts exercise every endpoint documented on the five API
reference pages.

| Group | Script | Endpoints shown |
|-------|--------|-----------------|
| Company Search | [`start_and_poll.py`](company_search/start_and_poll.py) | `start`, `status`, `get_search_result` |
| Company Search | [`instant_search.py`](company_search/instant_search.py) | `search` |
| Company Search | [`enrich.py`](company_search/enrich.py) | `start_enrichment` |
| Company Search | [`manage_lists.py`](company_search/manage_lists.py) | `get_lists`, `continue_`, `stop`, `stop_enrichment` |
| People Search | [`start_and_poll.py`](people_search/start_and_poll.py) | `start`, `status` |
| People Search | [`instant_search.py`](people_search/instant_search.py) | `search` |
| People Search | [`enrich_and_manage.py`](people_search/enrich_and_manage.py) | `continue_`, `start_enrichment`, `stop_enrichment`, `stop` |
| Deep Research | [`deep_research_stream.py`](research/deep_research_stream.py) | `start`, `stream`, `status` |
| Deep Research | [`respond_to_clarification.py`](research/respond_to_clarification.py) | `start`, `stream`, `respond` |
| Deep Research | [`active_and_stop.py`](research/active_and_stop.py) | `active`, `stop` |
| Enterprise Search | [`chat.py`](enterprise_search/chat.py) | `create_chat_session`, `send_chat_message` (stream + JSON) |
| Enterprise Search | [`sessions.py`](enterprise_search/sessions.py) | `create_chat_session`, `rename_chat_session`, `get_chat_sessions` |
| Enterprise Search | [`connectors.py`](enterprise_search/connectors.py) | `get_connector_status`, `get_connectors`, `get_cc_pair`, `update_cc_pair_status` (+ create/run-once/associate/delete) |
| Enterprise Search | [`upload_file.py`](enterprise_search/upload_file.py) | `upload_file`, `get_file_statuses` |
| Memory | [`departments_and_chat.py`](memory/departments_and_chat.py) | `create_department`, `upload`, `chat` |
| Memory | [`manage.py`](memory/manage.py) | `list_departments`, `get_department`, `ingest_connectors` |
| Memory | [`generate_memory.py`](memory/generate_memory.py) | `generate` |

> Deep Research also needs a service ID — set `CHORDIAN_SERVICE_ID` or pass
> `service_id=...`.
