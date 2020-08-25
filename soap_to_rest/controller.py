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
  if _is_array(d):
    array = _get_array_from_suds_object(d)
    return list(map(convert_value, array))
  else:
    key_value_entries = asdict(d).items()
    return dict(list(starmap(convert_entry, key_value_entries)))

def _get_class_name(sudso):
  return sudso.__class__.__name__

def _get_array_from_suds_object(sudso):
  return sudso[sudso.__keylist__[0]]

def _is_array(object):
  return 'Array' in _get_class_name(object)

def convert_entry(k, v):
  if hasattr(v, '__keylist__'):
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