import pytest
import json
import logging
logging.basicConfig(level=logging.WARNING)

from soap_to_rest import __version__
from tests.fake_wsdl_server import create_fake_server

from soap_to_rest.controller import app

pytestmark = pytest.mark.asyncio

async def test_version():
    client = app.test_client()

    url = create_fake_server()

    data = {
        'url': url,
        'action': 'say_hello',
        'params': {
            'name': 'Tim',
            'times': 2
        }
    }

    result = await client.post('/api/v1/wsdl', json=data)
    data = await result.get_json()

    assert len(data) == 2


