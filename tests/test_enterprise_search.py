import json

import httpx
from conftest import CORE

import chordian


def test_send_chat_message_non_stream(respx_mock):
    route = respx_mock.post(f"{CORE}/chat/send-chat-message").mock(
        return_value=httpx.Response(200, json={"answer": "hi"})
    )
    resp = chordian.EnterpriseSearch.send_chat_message(
        message="hello", chat_session_id="s1", include_citations=True
    )
    assert resp["answer"] == "hi"
    body = json.loads(route.calls.last.request.content)
    assert body == {
        "message": "hello",
        "chat_session_id": "s1",
        "stream": False,
        "include_citations": True,
    }


def test_send_chat_message_stream(respx_mock):
    sse = 'event: token\ndata: {"text": "hi"}\n\n'
    respx_mock.post(f"{CORE}/chat/send-chat-message").mock(
        return_value=httpx.Response(200, text=sse)
    )
    events = list(
        chordian.EnterpriseSearch.send_chat_message(
            message="hello", chat_session_id="s1", stream=True
        )
    )
    assert events[0].event == "token"
    assert events[0].json == {"text": "hi"}


def test_get_connectors_query_param(respx_mock):
    route = respx_mock.get(f"{CORE}/manage/admin/connector").mock(
        return_value=httpx.Response(200, json=[])
    )
    chordian.EnterpriseSearch.get_connectors(credential=7)
    assert route.calls.last.request.url.params["credential"] == "7"


def test_upload_file_multipart(respx_mock, tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("hello world")

    route = respx_mock.post(f"{CORE}/user/projects/file/upload").mock(
        return_value=httpx.Response(200, json={"user_files": [], "rejected_files": []})
    )
    chordian.EnterpriseSearch.upload_file(str(f))

    request = route.calls.last.request
    assert request.headers["content-type"].startswith("multipart/form-data")
    assert b"doc.txt" in request.content
    assert b"hello world" in request.content
