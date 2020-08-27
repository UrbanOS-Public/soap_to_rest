"""The main API controller for the soap_to_rest service"""
import logging

from quart import Quart, Response, jsonify, request
from schema import Optional, Regex, Schema, SchemaError, Use

from soap_to_rest.suds_converter import to_serializable
from soap_to_rest.wsdl_service import WsdlError, invoke_action
from soap_to_rest.custom_validators import is_web_url

WSDL_PARAMS_SCHEMA = Schema(
    {
        "url": Use(
            is_web_url, error="'url' must point to a valid URL that returns a WSDL"
        ),
        "action": str,
        Optional("params"): Use(dict, error="'params' must be an object"),
        Optional("auth"): Schema({"username": str, "password": str}),
    },
    name="WSDL Parameters",
)

logging.basicConfig(level=logging.WARNING)

app = Quart(__name__)


@app.route("/api/v1/wsdl", methods=["POST", "GET"])
async def wsdl():
    """
    Service endpoint for invoking an action on a
    web service defined by a WSDL
    """
    try:
        (url, action, params, auth) = await _validate_wsdl_params(request)
        result = invoke_action(url, action, params, auth)
        serializable_result = to_serializable(result)

        return jsonify(serializable_result)
    except SchemaError as schema_error:
        return _schema_error(schema_error)
    except WsdlError as wsdl_error:
        return _wsdl_error(wsdl_error)
    except TypeError as type_error:
        return _serialization_error(type_error)


async def _validate_wsdl_params(wsdl_request):
    request_body = await wsdl_request.json

    WSDL_PARAMS_SCHEMA.validate(request_body)

    url = request_body.get("url")
    action = request_body.get("action")
    params = request_body.get("params")
    auth = request_body.get("auth")

    return (url, action, params, auth)


def _schema_error(error):
    message = error.code
    logging.error(f"Failed to validate WSDL request parameters: {message}")
    return Response(message, status=400, mimetype="text/plain")


def _wsdl_error(error):
    message = f"Failed to invoke WSDL: {error.wrapped}"
    logging.error(message)
    return Response(message, status=400, mimetype="text/plain")


def _serialization_error(error):
    message = f"Failed to serialize SOAP response: {error}"
    logging.error(message)
    return Response(message, status=500, mimetype="text/plain")


if __name__ == "__main__":
    app.run()
