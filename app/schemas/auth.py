from pydantic import BaseModel


class AuthLinkSchema(BaseModel):
    auth_link: str


class AuthCredentialsSchema(BaseModel):
    address: str
    session_id: str
