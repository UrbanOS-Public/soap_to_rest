import logging

logging.basicConfig(level=logging.DEBUG)
from threading import Thread
from wsgiref.simple_server import make_server

from spyne import (
    Application,
    ComplexModel,
    Integer,
    Iterable,
    ServiceBase,
    String,
    Unicode,
    rpc,
)
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Person(ComplexModel):
    name = String
    address = String

    def __init__(self, name="person", address="personville"):
        self.name = name
        self.address = address


class Dog(ComplexModel):
    name = String
    address = String
    toys = Iterable(String)

    def __init__(self, name, address, toys=[]):
        self.name = name
        self.address = address
        self.toys = toys


class Neighborhood(ComplexModel):
    name = String
    people = Iterable(Person)
    dogs = Iterable(Dog)
    phone_numbers = Iterable(String)

    def __init__(self, name, people=[], dogs=[], phone_numbers=[]):
        self.name = name
        self.people = people
        self.dogs = dogs
        self.phone_numbers = phone_numbers


class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_my_name(ctx, name):
        return name

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield "Hello, %s" % name

    @rpc(Person, _returns=Dog)
    def person_to_dog(ctx, person):
        return Dog(person.name, person.address)

    @rpc(_returns=Iterable(Dog))
    def good_dogs(_ctx):
        return [
            Dog("Pi", "123 Bork Street", ["Food", "Socks"]),
            Dog("Cricket", "123 Bork Street", ["Llama"]),
        ]

    @rpc(_returns=Iterable(Neighborhood))
    def neighborhoods(_ctx):
        return [
            Neighborhood(
                "Meadows",
                [Dog("Pi", "123 Bork Street", ["Food", "Kitchen Towel"])],
                [Person("Joe", "123 American Way")],
                ["555-123-4567"],
            ),
            Neighborhood(
                "Montana",
                [Dog("Max", "123 Dump Road", ["Beggin Strips"])],
                [Person("Jim", "123 Western Way")],
                ["555-890-1234"],
            ),
        ]


application = Application(
    [HelloWorldService],
    tns="spyne.examples.hello",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)


def create_fake_server(port=8000, daemon=True):
    wsgi_app = WsgiApplication(application)
    server = make_server("0.0.0.0", port, wsgi_app)
    Thread(target=server.serve_forever, daemon=daemon).start()
    return f"http://localhost:{str(port)}?WSDL"


if __name__ == "__main__":
    create_fake_server(daemon=False)
