import json

import httpx
import pytest
from conftest import CORE

import chordian


def test_start_requires_service_id(respx_mock):
    with pytest.raises(ValueError):
        chordian.Research.start(query="hello")


def test_start_with_module_service_id(respx_mock):
    chordian.service_id = "svc-1"
    route = respx_mock.post(f"{CORE}/research/start").mock(
        return_value=httpx.Response(200, json={"thread_id": "r1", "status": "started"})
    )
    resp = chordian.Research.start(query="hello", allow_clarification=True)
    assert resp["thread_id"] == "r1"
    body = json.loads(route.calls.last.request.content)
    assert body["serviceId"] == "svc-1"
    assert body["allow_clarification"] is True


def test_respond_uses_query_param(respx_mock):
    route = respx_mock.post(f"{CORE}/research/respond/r1").mock(
        return_value=httpx.Response(200, json={"status": "processing"})
    )
    chordian.Research.respond("r1", "my answer")
    assert route.calls.last.request.url.params["response"] == "my answer"


def test_stop_uses_delete(respx_mock):
    route = respx_mock.delete(f"{CORE}/research/stop/r1").mock(
        return_value=httpx.Response(200, json={"status": "stopped"})
    )
    chordian.Research.stop("r1")
    assert route.calls.last.request.method == "DELETE"


def test_stream_parses_sse(respx_mock):
    sse_body = (
        "event: progress\n"
        'data: {"step": 1}\n'
        "\n"
        "event: complete\n"
        'data: {"final_report": "done"}\n'
        "\n"
    )
    respx_mock.get(f"{CORE}/research/stream/r1").mock(
        return_value=httpx.Response(
            200, text=sse_body, headers={"content-type": "text/event-stream"}
        )
    )
    events = list(chordian.Research.stream("r1"))
    assert [e.event for e in events] == ["progress", "complete"]
    assert events[0].json == {"step": 1}
    assert events[1].json == {"final_report": "done"}
