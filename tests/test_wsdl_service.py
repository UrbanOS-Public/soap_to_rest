# TODO - UNIT test the auth part with mocks as spyne doesn't do WSSE easily
import re
from xml.sax import SAXParseException
from xml.sax.xmlreader import Locator

import pytest
from mockito import any
from suds import MethodNotFound, WebFault
from suds.transport import TransportError

import soap_to_rest.wsdl_service as wsdl_service


def test_unactionable_errors(when):
    internal_error_message = "something the user should NOT see"

    when(wsdl_service).Client(any).thenRaise(Exception(internal_error_message))

    with pytest.raises(wsdl_service.WsdlError) as we:
        wsdl_service.invoke_action("a url", "an action", {})

    assert internal_error_message not in str(we)


class Fault:
    def __init__(self, faultcode, faultstring):
        self.faultstring = faultstring
        self.faultcode = faultcode


errors_to_test = [
    (TransportError("disregard", 404), r"error.*wsdl.*404"),
    (SAXParseException("disregard", None, Locator()), r"error.*parsing.*wsdl"),
    (MethodNotFound("whonko"), r"action.*whonko.*not.*found"),
    (
        WebFault(
            Fault(
                "soap11env:Client.SchemaValidationError", "this is the full fault text"
            ),
            None,
        ),
        r"error.*this is the full fault text",
    ),
    (
        WebFault(Fault("InvalidSecurity", "this is the full fault text"), None),
        r"authentication.*error.*this is the full fault text",
    ),
    (TypeError("this is the full error text"), r"error.*this is the full error text"),
]
error_test_ids = [
    "TransportError",
    "SAXParseException",
    "MethodNotFound",
    "WebFault[SchemaValidation]",
    "WebFault[Authentication]",
    "TypeError",
]


@pytest.mark.parametrize("error,message", errors_to_test, ids=error_test_ids)
def test_parameters(error, message, when):
    when(wsdl_service).Client(any).thenRaise(error)

    with pytest.raises(wsdl_service.WsdlError) as we:
        wsdl_service.invoke_action("a url", "whonko", {})

    assert re.search(message, str(we), re.IGNORECASE)
