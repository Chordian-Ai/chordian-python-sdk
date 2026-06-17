import json

import httpx
from conftest import MEMORY

import chordian


def test_chat_routes_to_memory_base_url(respx_mock):
    route = respx_mock.post(f"{MEMORY}/memory/chat").mock(
        return_value=httpx.Response(200, json={"answer": "yes", "nodes": [], "edges": []})
    )
    resp = chordian.Memory.chat(list_id="L1", question="what?")
    assert resp["answer"] == "yes"
    request = route.calls.last.request
    # Routed to the memory base URL, not the core one.
    assert str(request.url).startswith(MEMORY)
    body = json.loads(request.content)
    assert body == {"listId": "L1", "question": "what?"}


def test_list_departments(respx_mock):
    respx_mock.get(f"{MEMORY}/memory/departments").mock(
        return_value=httpx.Response(200, json={"departments": [{"graph_id": "g1"}]})
    )
    resp = chordian.Memory.list_departments()
    assert resp["departments"][0]["graph_id"] == "g1"


def test_create_department_drops_none(respx_mock):
    route = respx_mock.post(f"{MEMORY}/memory/departments/create").mock(
        return_value=httpx.Response(200, json={"graph_id": "g2"})
    )
    chordian.Memory.create_department(name="Sales")
    body = json.loads(route.calls.last.request.content)
    assert body == {"name": "Sales"}


def test_upload_multipart_with_list_id(respx_mock, tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("a,b\n1,2\n")
    route = respx_mock.post(f"{MEMORY}/memory/upload").mock(
        return_value=httpx.Response(200, json={"jobId": "j1", "status": "queued"})
    )
    chordian.Memory.upload(file=str(f), list_id="L1")
    content = route.calls.last.request.content
    assert b"data.csv" in content
    assert b"L1" in content


def test_generate_camel_case_keys(respx_mock):
    route = respx_mock.post(f"{MEMORY}/memory/generate").mock(
        return_value=httpx.Response(200, json={"jobId": "j2", "status": "queued"})
    )
    chordian.Memory.generate(
        list_id="L1",
        records=[{"cells": {"x": 1}}],
        columns=[{"id": "x", "header": "X", "type": "number"}],
        workflow_category="company",
    )
    body = json.loads(route.calls.last.request.content)
    assert body["listId"] == "L1"
    assert body["workflowCategory"] == "company"
