import json
import re

import pytest
from dpath.util import values as get_in
from fastapi.testclient import TestClient
from mockito import any, mock

import soap_to_rest
from soap_to_rest import app
from soap_to_rest.wsdl_service import WsdlError
from tests.fake_wsdl_server import create_fake_server

client = TestClient(app)


@pytest.fixture(scope="module")
def fake_wsdl_server_url():
    return create_fake_server()


def test_single_primordial_type(fake_wsdl_server_url):
    data = {
        "url": fake_wsdl_server_url,
        "action": "say_my_name",
        "params": {"name": "Tim"},
    }

    result = client.post("/api/v1/wsdl", json=data)
    data = result.json()

    assert ["Tim"] == data


def test_multiple_primordial_types(fake_wsdl_server_url):
    data = {
        "url": fake_wsdl_server_url,
        "action": "say_hello",
        "params": {"name": "Tim", "times": 2},
    }

    result = client.post("/api/v1/wsdl", json=data)
    data = result.json()

    assert ["Hello Tim", "Hello Tim"]


def test_single_object(fake_wsdl_server_url):
    data = {
        "url": fake_wsdl_server_url,
        "action": "person_to_dog",
        "params": {"person": {"name": "Ben", "address": "123 Garage Street"}},
    }

    result = client.post("/api/v1/wsdl", json=data)
    data = result.json()

    assert {"name": "Ben", "address": "123 Garage Street", "toys": None} == data


def test_multiple_objects(fake_wsdl_server_url):
    data = {"url": fake_wsdl_server_url, "action": "good_dogs", "params": {}}

    result = client.post("/api/v1/wsdl", json=data)
    data = result.json()

    assert [
        {"name": "Pi", "address": "123 Bork Street", "toys": ["Food", "Socks"]},
        {"name": "Cricket", "address": "123 Bork Street", "toys": ["Llama"]},
    ] == data


def test_nested_objects(fake_wsdl_server_url):
    data = {"url": fake_wsdl_server_url, "action": "neighborhoods", "params": {}}

    result = client.post("/api/v1/wsdl", json=data)
    data = result.json()

    assert data != None


params_to_test = [
    ({"url": "http://example.com?WSDL"}, ["action"], ["field required"]),
    ({"action": "do-it"}, ["url"], ["field required"]),
    ({}, ["url", "action"], ["field required", "field required"]),
    (
        {"url": "http://example.com?WSDL", "action": "do-it", "params": "WRONGO"},
        ["params"],
        ["value is not a valid dict"],
    ),
    (
        {"url": "not_a_url", "action": "do-it"},
        ["url"],
        ["invalid or missing URL scheme"],
    ),
    (
        {"url": "file:///etc/passwd", "action": "do-it"},
        ["url"],
        ["URL scheme not permitted"],
    ),
    (
        {"url": "http://example.com?WSDL", "action": "do-it", "auth": {}},
        ["username", "password"],
        ["field required", "field required"],
    ),
]


@pytest.mark.parametrize("params,fields,messages", params_to_test)
def test_parameters(params, fields, messages):
    result = client.post("/api/v1/wsdl", json=params)

    assert 422 == result.status_code
    body = result.json()

    actual_fields = [
        f for f in get_in(body, "/detail/*/loc/*") if f not in ["body", "auth"]
    ]
    actual_messages = get_in(body, "/detail/*/msg")

    assert fields == actual_fields
    assert messages == actual_messages


def test_wsdl_errors(when, fake_wsdl_server_url):
    when(soap_to_rest).invoke_action(any(str), any(str), any(dict), None).thenRaise(
        WsdlError(Exception("baddies"))
    )
    data = {"url": fake_wsdl_server_url, "action": "neighborhoods", "params": {}}
    result = client.post("/api/v1/wsdl", json=data)

    assert 400 == result.status_code
    body = result.json()
    assert re.search(r"failed.*wsdl", body["msg"], flags=re.IGNORECASE | re.MULTILINE)


def test_serialization_errors(when, fake_wsdl_server_url):
    when(soap_to_rest).to_serializable(any).thenReturn(dict)

    data = {"url": fake_wsdl_server_url, "action": "neighborhoods", "params": {}}
    result = client.post("/api/v1/wsdl", json=data)

    assert 500 == result.status_code
    body = result.json()
    assert re.search(
        r"failed.*serialize", body["msg"], flags=re.IGNORECASE | re.MULTILINE
    )
