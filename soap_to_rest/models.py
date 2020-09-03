"""
Models for input and domain for the application
"""
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel


class AuthParams(BaseModel):
    """
    Authentication parameters for conversion to WSSE, etc.
    """
    username: str
    password: str


class WsdlRequest(BaseModel):
    """
    The main wsdl API request model, largely for validation.
    """
    url: AnyHttpUrl
    action: str
    params: Optional[dict] = {}
    auth: Optional[AuthParams] = None
