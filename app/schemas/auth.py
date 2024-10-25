from pydantic import BaseModel


class AuthResponceSchema(BaseModel):
    token: str
    auth_link: str


class CheckAuthSchema(BaseModel):
    address: str
