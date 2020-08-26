from quart import Quart
from quart import jsonify
from quart import request

from suds.client import Client
from suds.wsse import *
import json

from itertools import starmap
from soap_to_rest.suds_converter import suds_to_serializable

import logging
logging.basicConfig(level=logging.WARNING)

app = Quart(__name__)


@app.route('/api/v1/wsdl', methods=['POST'])
async def wsdl():
  request_body = await request.json
  url = request_body.get('url')
  action = request_body.get('action')
  params = request_body.get('params')
  auth = request_body.get('auth')

  if auth:
    security = Security()
    token = UsernameToken(auth['username'], auth['password'])
    security.tokens.append(token)
    client = Client(url, wsse=security)
  else:
    client = Client(url)

  results = client.service.__getattr__(action)(**params)

  return jsonify(suds_to_serializable(results))


if __name__ == '__main__':
  app.run()