from quart import Quart
from quart import jsonify
from quart import request

from suds.client import Client
from suds.wsse import *
import json

from itertools import starmap

import logging
logging.basicConfig(level=logging.WARNING)

app = Quart(__name__)

from suds.sudsobject import asdict


def recursive_asdict(d):
  class_name = d.__class__.__name__
  logging.warning(class_name)
  if 'Array' not in class_name:
    logging.warning('Thingy')
    return dict(list(starmap(convert_entry, asdict(d).items())))
  else:
    thing = d[d.__keylist__[0]]
    return list(map(convert_value, thing))


def convert_entry(k, v):
  logging.warning("Converting entry")
  if hasattr(v, '__keylist__'):
    class_name = v.__class__.__name__
    if 'Array' in class_name:
      thing = v[v.__keylist__[0]]
      return (k, list(map(convert_value, thing)))
    else:
      return (k, recursive_asdict(v))
  elif isinstance(v, list): 
    return list(map(convert_value, v))
  else:
    return (k, v)

    
def convert_value(v):
  logging.warning(f"Converting Value: {v}")
  if hasattr(v, '__keylist__'):
      return recursive_asdict(v)
  else:
      return v


def suds_to_json(data):
    if hasattr(data, '__dict__'):
      data = recursive_asdict(data)
    else:
      data = [data]
    logging.warning(data)
    return jsonify(data)


@app.route('/api/v1/wsdl', methods=['POST'])
async def wsdl():
  request_body = await request.json
  url = request_body.get('url')
  action = request_body.get('action')
  params = request_body.get('params')
  client = Client(url)
  results = client.service.__getattr__(action)(**params)

  return suds_to_json(results)


if __name__ == '__main__':
  app.run()