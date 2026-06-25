import json

import httpx
import pytest
from conftest import CORE

import chordian


def test_start_sends_bearer_and_body(respx_mock):
    route = respx_mock.post(f"{CORE}/agentic-crawler/start").mock(
        return_value=httpx.Response(
            200,
            json={
                "success": True,
                "thread_id": "t1",
                "websocket_url": "wss://agent.example/ws",
                "status": "ready",
            },
        )
    )

    resp = chordian.AgenticCrawler.start(
        prompt="Find US beauty brands",
        thread_id="t1",
    )

    assert resp["thread_id"] == "t1"
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer on_tenant_99999.testtoken"
    body = json.loads(request.content)
    assert body == {"prompt": "Find US beauty brands", "thread_id": "t1"}


def test_empty_prompt_raises(respx_mock):
    with pytest.raises(ValueError, match="prompt must not be empty"):
        chordian.AgenticCrawler.start(prompt="   ")


def test_whitespace_prompt_is_stripped(respx_mock):
    route = respx_mock.post(f"{CORE}/agentic-crawler/start").mock(
        return_value=httpx.Response(200, json={"success": True, "thread_id": "t1"})
    )
    chordian.AgenticCrawler.start(prompt="  find brands  ")
    body = json.loads(route.calls.last.request.content)
    assert body["prompt"] == "find brands"
