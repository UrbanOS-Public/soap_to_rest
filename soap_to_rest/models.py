from pydantic import BaseModel, AnyHttpUrl
from typing import Optional

class AuthParams(BaseModel):
  username: str
  password: str


class WsdlRequest(BaseModel):
    url: AnyHttpUrl
    action: str
    params: Optional[dict] = {}
    auth: Optional[AuthParams] = None