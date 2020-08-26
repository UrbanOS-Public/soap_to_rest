"""Module for working with a wsdl and resulting web service"""
import logging
from xml.sax import SAXParseException

from suds import MethodNotFound, WebFault
from suds.client import Client
from suds.transport import TransportError
from suds.wsse import Security, UsernameToken


class WsdlError(Exception):
    """Simple wrapper for any errors occurring during web service invocation"""

    def __init__(self, wsdl_error):
        super().__init__()
        self.wrapped = wsdl_error


def invoke_action(url, action, params, auth=None):
    """Invokes an action contained in the provided WSDL url using provided parameters"""
    try:
        if auth:
            security = Security()
            token = UsernameToken(auth["username"], auth["password"])
            security.tokens.append(token)
            client = Client(url, wsse=security)
        else:
            client = Client(url)

        return client.service.__getattr__(action)(**params)

    except TransportError as tex:
        _raise_wsdl_error(
            f"Error accessing WSDL at {url}, got HTTP status code {tex.httpcode}"
        )
    except SAXParseException:
        _raise_wsdl_error(
            f"Error parsing the WSDL at {url}, please contact WSDL provider"
        )
    except MethodNotFound:
        _raise_wsdl_error(f"Action {action} not found")
    except WebFault as web_fault:
        if web_fault.fault.faultcode == "InvalidSecurity":
            _raise_wsdl_error(
                f"Authentication error when invoking action {action}, {web_fault.fault.faultstring}"
            )
        _raise_wsdl_error(
            f"Error invoking action {action}, {web_fault.fault.faultstring}"
        )
    except TypeError as type_error:
        _raise_wsdl_error(f"Error invoking action {action}, {type_error}")
    except Exception as ex:
        logging.error(
            f"Wsdl error occurred that we won't send to users: {type(ex)} {ex}"
        )
        _raise_wsdl_error(
            "Error occurred while processing wsdl, please contact this API's maintainers"
        )


def _raise_wsdl_error(message):
    logging.warning(message)
    raise WsdlError(Exception(message))
