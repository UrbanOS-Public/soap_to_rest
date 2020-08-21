import logging
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, String, ComplexModel
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from threading import Thread

class Person(ComplexModel):
  name = String
  address = String

  def __init__(self):
    self.name = 'person'
    self.address = 'personville'

class Dog(ComplexModel):
  name = String
  address = String

  def __init__(self, name, address):
    self.name = name
    self.address = address

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name

    @rpc(Person, _returns=Dog)
    def person_to_dog(ctx, person):
      return Dog(person.name, person.address)

application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)


def create_fake_server(port=8000, daemon=True):
  wsgi_app = WsgiApplication(application)
  server = make_server('0.0.0.0', port, wsgi_app)
  Thread(target=server.serve_forever, daemon=daemon).start()
  return f'http://localhost:{str(port)}?WSDL'
  

if __name__ == '__main__':
  create_fake_server(daemon=False)