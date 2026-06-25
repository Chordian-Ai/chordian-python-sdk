import httpx
import pytest
from conftest import CORE

import chordian
from chordian.exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    NoApiKeyError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


def test_no_api_key_raises(respx_mock, monkeypatch):
    monkeypatch.delenv("CHORDIAN_API_KEY", raising=False)
    chordian.api_key = None
    with pytest.raises(NoApiKeyError):
        chordian.CompanySearch.get_lists()


def test_api_key_from_env(respx_mock, monkeypatch):
    chordian.api_key = None
    monkeypatch.setenv("CHORDIAN_API_KEY", "on_tenant_1.envtoken")
    route = respx_mock.get(f"{CORE}/company-search/getLists").mock(
        return_value=httpx.Response(200, json={"success": True, "data": [], "total": 0})
    )
    chordian.CompanySearch.get_lists()
    assert route.calls.last.request.headers["authorization"] == "Bearer on_tenant_1.envtoken"


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, AuthenticationError),
        (404, NotFoundError),
        (422, ValidationError),
        (429, RateLimitError),
        (500, ServerError),
    ],
)
def test_error_status_mapping(respx_mock, status, exc):
    respx_mock.get(f"{CORE}/company-search/getLists").mock(
        return_value=httpx.Response(status, json={"detail": "boom"})
    )
    with pytest.raises(exc) as info:
        chordian.CompanySearch.get_lists()
    assert info.value.status_code == status
    assert "boom" in str(info.value)


def test_timeout_wrapped(respx_mock):
    respx_mock.get(f"{CORE}/company-search/getLists").mock(
        side_effect=httpx.ReadTimeout("timed out")
    )
    with pytest.raises(APITimeoutError):
        chordian.CompanySearch.get_lists()


def test_connection_error_wrapped(respx_mock):
    respx_mock.get(f"{CORE}/company-search/getLists").mock(
        side_effect=httpx.ConnectError("no route")
    )
    with pytest.raises(APIConnectionError):
        chordian.CompanySearch.get_lists()


def test_base_url_override(respx_mock):
    chordian.core_base_url = "https://staging.example.com"
    route = respx_mock.get("https://staging.example.com/company-search/getLists").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    chordian.CompanySearch.get_lists()
    assert route.called


def test_fastapi_validation_detail_formatted(respx_mock):
    respx_mock.get(f"{CORE}/company-search/getLists").mock(
        return_value=httpx.Response(
            422,
            json={
                "detail": [
                    {
                        "loc": ["body", "proxy_country_code"],
                        "msg": "Field required",
                        "type": "value_error",
                    }
                ]
            },
        )
    )
    with pytest.raises(ValidationError) as info:
        chordian.CompanySearch.get_lists()
    assert str(info.value) == "[422] proxy_country_code: Field required"
