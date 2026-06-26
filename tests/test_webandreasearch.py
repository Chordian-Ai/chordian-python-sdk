import json

import httpx
import pytest
from conftest import CORE

import chordian


def test_start_sends_required_fields(respx_mock):
    route = respx_mock.post(f"{CORE}/webandreasearch/start").mock(
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

    resp = chordian.WebAndResearch.start(
        prompt="Research fintech startups in India",
        live_url=False,
        proxy=False,
        llm_model="chordian-r1",
    )

    assert resp["thread_id"] == "t1"
    body = json.loads(route.calls.last.request.content)
    assert body == {
        "prompt": "Research fintech startups in India",
        "live_url": False,
        "proxy": False,
        "llm_model": "chordian-r1",
    }


def test_empty_prompt_raises(respx_mock):
    with pytest.raises(ValueError, match="prompt must not be empty"):
        chordian.WebAndResearch.start(
            prompt="  ",
            live_url=False,
            proxy=False,
            llm_model="chordian-r1",
        )


def test_invalid_llm_model_raises(respx_mock):
    with pytest.raises(ValueError, match="llm_model must be one of"):
        chordian.WebAndResearch.start(
            prompt="search",
            live_url=False,
            proxy=False,
            llm_model="gpt-4",
        )


def test_proxy_requires_country_code(respx_mock):
    with pytest.raises(ValueError, match="proxy_country_code is required"):
        chordian.WebAndResearch.start(
            prompt="search",
            live_url=True,
            proxy=True,
            llm_model="chordian-r1",
        )
