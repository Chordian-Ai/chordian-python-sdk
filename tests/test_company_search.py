import json

import httpx
from conftest import CORE

import chordian


def test_start_sends_bearer_and_body(respx_mock):
    route = respx_mock.post(f"{CORE}/company-search/start").mock(
        return_value=httpx.Response(
            200, json={"success": True, "thread_id": "t1", "status": "started"}
        )
    )

    resp = chordian.CompanySearch.start(
        prompt="AI startups", list_name="My List", search_mode="fast"
    )

    assert resp["thread_id"] == "t1"
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer on_tenant_99999.testtoken"
    assert request.headers["content-type"] == "application/json"
    body = json.loads(request.content)
    # None values must be dropped from the body.
    assert body == {"prompt": "AI startups", "list_name": "My List", "search_mode": "fast"}


def test_status_uses_path_param(respx_mock):
    respx_mock.get(f"{CORE}/company-search/status/abc").mock(
        return_value=httpx.Response(200, json={"status": "running"})
    )
    resp = chordian.CompanySearch.status("abc")
    assert resp["status"] == "running"


def test_search_post_body(respx_mock):
    route = respx_mock.post(f"{CORE}/company-search/search").mock(
        return_value=httpx.Response(200, json={"results": [], "count": 0})
    )
    chordian.CompanySearch.search(query="stripe.com", limit=5, path=["website"])
    body = json.loads(route.calls.last.request.content)
    assert body == {"query": "stripe.com", "limit": 5, "path": ["website"]}


def test_continue_underscore_method(respx_mock):
    route = respx_mock.post(f"{CORE}/company-search/continue").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    chordian.CompanySearch.continue_(thread_id="t1", total_target=100)
    body = json.loads(route.calls.last.request.content)
    assert body == {"thread_id": "t1", "total_target": 100}
