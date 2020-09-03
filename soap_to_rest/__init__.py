"""The main API controller for the soap_to_rest service"""
import logging

import uvicorn
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

from soap_to_rest.models import WsdlRequest
from soap_to_rest.suds_converter import to_serializable
from soap_to_rest.wsdl_service import WsdlError, invoke_action

LOGGER = logging.getLogger(__name__)


logging.basicConfig(level=logging.WARNING)

app = FastAPI()


@app.post("/api/v1/wsdl", status_code=status.HTTP_200_OK)
def wsdl(request: WsdlRequest):
    """
    Service endpoint for invoking an action on a
    web service defined by a WSDL
    """
    try:
        result = invoke_action(
            request.url, request.action, request.params, request.auth
        )
        serializable_result = to_serializable(result)
        return JSONResponse(content=serializable_result)
    except WsdlError as wsdl_error:
        return _wsdl_error(wsdl_error)
    except TypeError as type_error:
        return _serialization_error(type_error)


def _wsdl_error(error):
    message = f"Failed to invoke WSDL: {error.wrapped}"
    LOGGER.error(message)
    return JSONResponse(
        content=_error_message(message),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def _serialization_error(error):
    message = f"Failed to serialize SOAP response: {error}"
    LOGGER.error(message)
    return JSONResponse(
        content=_error_message(message),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _error_message(message):
    return {"msg": message}


if __name__ == "__main__":
    uvicorn.run("soap_to_rest:app", host="127.0.0.1", port=5000, log_level="info")
