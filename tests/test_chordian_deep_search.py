import json

import httpx
import pytest
from conftest import CORE

import chordian


def test_start_sends_body(respx_mock):
    route = respx_mock.post(f"{CORE}/chordian-deep-search/start").mock(
        return_value=httpx.Response(
            200,
            json={
                "success": True,
                "thread_id": "t1",
                "websocket_url": "wss://agent.example/ws/t1",
                "status": "processing",
            },
        )
    )

    resp = chordian.ChordianDeepSearch.start(
        prompt="find Kerala AI startups",
        llm_model="claude-sonnet-4.6",
        live_url=True,
        proxy=False,
    )

    assert resp["thread_id"] == "t1"
    body = json.loads(route.calls.last.request.content)
    assert body == {
        "prompt": "find Kerala AI startups",
        "llm_model": "claude-sonnet-4.6",
        "live_url": True,
        "proxy": False,
    }


def test_empty_prompt_raises(respx_mock):
    with pytest.raises(ValueError, match="prompt must not be empty"):
        chordian.ChordianDeepSearch.start(prompt="")


def test_proxy_requires_country_code(respx_mock):
    with pytest.raises(ValueError, match="proxy_country_code is required"):
        chordian.ChordianDeepSearch.start(
            prompt="search",
            proxy=True,
            live_url=True,
        )


def test_proxy_requires_live_url(respx_mock):
    with pytest.raises(ValueError, match="live_url must be true when proxy is true"):
        chordian.ChordianDeepSearch.start(
            prompt="search",
            proxy=True,
            live_url=False,
            proxy_country_code="us",
        )


def test_upload_sends_multipart(respx_mock):
    route = respx_mock.post(f"{CORE}/chordian-deep-search/upload").mock(
        return_value=httpx.Response(
            200,
            json={"success": True, "workspace_id": "ws1", "paths": ["uploads/a.md"]},
        )
    )

    resp = chordian.ChordianDeepSearch.upload(
        ("document.md", b"# hello"),
        thread_id="t1",
    )

    assert resp["workspace_id"] == "ws1"
    request = route.calls.last.request
    assert "multipart/form-data" in request.headers["content-type"]
    assert b'name="file"' in request.content
    assert b'name="thread_id"' in request.content
