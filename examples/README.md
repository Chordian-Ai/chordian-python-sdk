# Examples

One script per API method — each example calls a **single** endpoint so you can
copy exactly the call you need. Every method documented on the five API reference
pages has its own file.

```bash
pip install chordian
export CHORDIAN_API_KEY="on_tenant_12345.xxxxxxxx"
python examples/company_search/search.py
```

Scripts that act on an existing resource take its id as a command-line argument,
e.g. `python examples/company_search/status.py <thread_id>`. Deep Research also
needs `CHORDIAN_SERVICE_ID`.

## Company Search (`/company-search/*`)
`start.py` · `continue_search.py` · `status.py` · `stop.py` · `start_enrichment.py` · `stop_enrichment.py` · `get_lists.py` · `get_search_result.py` · `search.py`

## People Search (`/people-search/*`)
`start.py` · `continue_search.py` · `status.py` · `stop.py` · `start_enrichment.py` · `stop_enrichment.py` · `search.py`

## Deep Research (`/research/*`)
`start.py` · `stream.py` · `status.py` · `active.py` · `respond.py` · `stop.py`

## Enterprise Search (`/chat/*`, `/manage/*`, `/user/projects/*`)
`send_chat_message.py` · `create_chat_session.py` · `get_chat_sessions.py` · `rename_chat_session.py` · `get_connector_status.py` · `get_connectors.py` · `create_connector.py` · `get_cc_pair.py` · `update_cc_pair_status.py` · `connector_run_once.py` · `create_deletion_attempt.py` · `associate_credential.py` · `upload_file.py` · `get_file_statuses.py`

## Memory (`/memory/*`)
`list_departments.py` · `get_department.py` · `create_department.py` · `upload.py` · `ingest_connectors.py` · `generate.py` · `chat.py`

## Notes
- These make **real authenticated calls** and consume credits — set a valid `CHORDIAN_API_KEY`.
- `CompanySearch.start`/`continue_` and `PeopleSearch.start`/`continue_` block server-side; those examples set `chordian.timeout = 300`.
- Streaming examples (`research/stream.py`, `enterprise_search/send_chat_message.py`) set `chordian.timeout = None`.
