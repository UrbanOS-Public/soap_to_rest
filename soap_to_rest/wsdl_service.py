from suds.client import Client
from suds.wsse import *

def invoke_action(url, action, params, auth = None):
  if auth:
    security = Security()
    token = UsernameToken(auth['username'], auth['password'])
    security.tokens.append(token)
    client = Client(url, wsse=security)
  else:
    client = Client(url)

  return client.service.__getattr__(action)(**params)