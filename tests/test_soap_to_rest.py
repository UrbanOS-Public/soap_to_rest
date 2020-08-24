import pytest
import json
import logging
logging.basicConfig(level=logging.WARNING)

from soap_to_rest import __version__
from tests.fake_wsdl_server import create_fake_server

from soap_to_rest.controller import app

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
def fake_wsdl_server_url():
    return create_fake_server()


async def test_single_primordial_type(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        'url': fake_wsdl_server_url,
        'action': 'say_my_name',
        'params': {
            'name': 'Tim'
        }
    }

    result = await client.post('/api/v1/wsdl', json=data)
    data = await result.get_json()

    assert ['Tim'] == data


async def test_multiple_primordial_types(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        'url': fake_wsdl_server_url,
        'action': 'say_hello',
        'params': {
            'name': 'Tim',
            'times': 2
        }
    }

    result = await client.post('/api/v1/wsdl', json=data)
    data = await result.get_json()

    assert ["Hello Tim", "Hello Tim"]


async def test_single_object(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        'url': fake_wsdl_server_url,
        'action': 'person_to_dog',
        'params': {
            'person': {
                'name': 'Ben',
                'address': '123 Garage Street'
            }
        }
    }

    result = await client.post('/api/v1/wsdl', json=data)
    data = await result.get_json()

    assert {
        'name': 'Ben',
        'address': '123 Garage Street',
        'toys': None
    } == data


async def test_multiple_objects(fake_wsdl_server_url):
    client = app.test_client()

    data = {
        'url': fake_wsdl_server_url,
        'action': 'good_dogs',
        'params': {}
    }

    result = await client.post('/api/v1/wsdl', json=data)
    data = await result.get_json()

    assert [
        {
            'name': 'Pi',
            'address': '123 Bork Street',
            'toys': ['Food', 'Socks']
        },
        {
            'name': 'Cricket',
            'address': '123 Bork Street',
            'toys': ['Llama']
        }
    ] == data