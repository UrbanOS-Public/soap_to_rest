import json
import logging
import re

import pytest
from mockito import any

logging.basicConfig(level=logging.WARNING)

import soap_to_rest.controller
from soap_to_rest import __version__
from soap_to_rest.controller import app
from soap_to_rest.wsdl_service import WsdlError
from tests.fake_wsdl_server import create_fake_server

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
def fake_wsdl_server_url():
    return create_fake_server()


async def test_single_primordial_type(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        "url": fake_wsdl_server_url,
        "action": "say_my_name",
        "params": {"name": "Tim"},
    }

    result = await client.post("/api/v1/wsdl", json=data)
    data = await result.get_json()

    assert ["Tim"] == data


async def test_multiple_primordial_types(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        "url": fake_wsdl_server_url,
        "action": "say_hello",
        "params": {"name": "Tim", "times": 2},
    }

    result = await client.post("/api/v1/wsdl", json=data)
    data = await result.get_json()

    assert ["Hello Tim", "Hello Tim"]


async def test_single_object(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        "url": fake_wsdl_server_url,
        "action": "person_to_dog",
        "params": {"person": {"name": "Ben", "address": "123 Garage Street"}},
    }

    result = await client.post("/api/v1/wsdl", json=data)
    data = await result.get_json()

    assert {"name": "Ben", "address": "123 Garage Street", "toys": None} == data


async def test_multiple_objects(fake_wsdl_server_url):
    client = app.test_client()

    data = {"url": fake_wsdl_server_url, "action": "good_dogs", "params": {}}

    result = await client.post("/api/v1/wsdl", json=data)
    data = await result.get_json()

    assert [
        {"name": "Pi", "address": "123 Bork Street", "toys": ["Food", "Socks"]},
        {"name": "Cricket", "address": "123 Bork Street", "toys": ["Llama"]},
    ] == data


async def test_nested_objects(fake_wsdl_server_url):
    client = app.test_client()

    data = {"url": fake_wsdl_server_url, "action": "neighborhoods", "params": {}}

    result = await client.post("/api/v1/wsdl", json=data)
    data = await result.get_json()

    assert data != None


params_to_test = [
    ({"url": "http://example.com?WSDL"}, 400, r"missing.*action"),
    ({"action": "do-it"}, 400, r"missing.*url"),
    ({}, 400, r"missing.*(action|url)+.*(action|url)+"),
    (
        {"url": "http://example.com?WSDL", "action": "do-it", "params": "WRONGO"},
        400,
        r"params.*object",
    ),
    ({"url": "not_a_url", "action": "do-it"}, 400, r"url.*valid.*wsdl"),
    (
        {"url": "http://example.com?WSDL", "action": "do-it", "auth": {}},
        400,
        r"missing.*(username|password)+.*(username|password)+",
    ),
]


@pytest.mark.parametrize("params,status,message", params_to_test)
async def test_parameters(params, status, message):
    client = app.test_client()

    result = await client.post("/api/v1/wsdl", json=params)

    assert status == result.status_code
    raw_body = await result.get_data()
    body = raw_body.decode()
    assert re.search(message, body, flags=re.IGNORECASE)


async def test_wsdl_errors(when, fake_wsdl_server_url):
    client = app.test_client()

    when(soap_to_rest.controller).invoke_action(
        any(str), any(str), any(dict), None
    ).thenRaise(WsdlError(Exception("baddies")))
    data = {"url": fake_wsdl_server_url, "action": "neighborhoods", "params": {}}
    result = await client.post("/api/v1/wsdl", json=data)

    assert 400 == result.status_code
    raw_body = await result.get_data()
    body = raw_body.decode()
    assert re.search(r"failed.*wsdl", body, flags=re.IGNORECASE | re.MULTILINE)


# TODO - conversion errors
