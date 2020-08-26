from suds.client import Client
from suds.wsse import *


class WsdlError(Exception):
  """Simple wrapper for any errors occurring during web service invocation"""
  def __init__(self, wsdl_error):
    self.wrapped = wsdl_error


def invoke_action(url, action, params, auth = None):
  try:
    if auth:
      security = Security()
      token = UsernameToken(auth['username'], auth['password'])
      security.tokens.append(token)
      client = Client(url, wsse=security)
    else:
      client = Client(url)

    return client.service.__getattr__(action)(**params)

  except Exception as ex:
    raise WsdlError(ex)