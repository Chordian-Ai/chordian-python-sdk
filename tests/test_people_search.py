import json

import httpx
from conftest import CORE

import chordian


def test_start(respx_mock):
    route = respx_mock.post(f"{CORE}/people-search/start").mock(
        return_value=httpx.Response(200, json={"thread_id": "p1"})
    )
    resp = chordian.PeopleSearch.start(prompt="CTOs in fintech")
    assert resp["thread_id"] == "p1"
    body = json.loads(route.calls.last.request.content)
    assert body == {"prompt": "CTOs in fintech"}


def test_search(respx_mock):
    route = respx_mock.post(f"{CORE}/people-search/search").mock(
        return_value=httpx.Response(200, json={"results": [], "count": 0})
    )
    chordian.PeopleSearch.search(query="Jane", limit=3, path=["fullName"])
    body = json.loads(route.calls.last.request.content)
    assert body["limit"] == 3
