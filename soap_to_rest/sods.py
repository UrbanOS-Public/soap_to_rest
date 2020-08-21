import logging
from suds.client import Client
from suds.wsse import *
from suds.plugin import *

security = Security()
token = UsernameToken('benjaminbrewer', 'password123')
security.tokens.append(token)

# url = 'https://webservices.chargepoint.com/cp_api_5.0.wsdl'
url = 'http://localhost:8000?WSDL'
action = 'person_to_dog'
params = {
  'person': {
    'name': 'stuff',
    'address': 'thing'
  }
}

def _tupleythrice(y):
  [param_name, params, _childparams] = y
  print(params)
  return params.type[0] # if not from the main http://www.w3.org/2001/XMLSchema

def _tupleytoo(y):
  [action, args] = y
  return (action, list(map(_tupleythrice, args)))

def _tupley(y):
  (_action, args) = y
  return list(map(_tupleytoo, args))

client = Client(url)
print(client.service.__getattr__(action)(**params))

# person = client.factory.create('Person')
# person['name'] = 'vincent adultman'
# person['address'] = 'personville'