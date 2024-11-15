from pydantic import BaseModel


class AuthLinkPayload(BaseModel):
    auth_link: str


class AuthLinkSchema(BaseModel):
    type: str = "auth_link"
    payload: AuthLinkPayload


class AuthSuccessPayload(BaseModel):
    address: str
    session_id: str


class AuthSuccessSchema(BaseModel):
    type: str = "auth_success"
    payload: AuthSuccessPayload


class AuthUserRejectsSchema(BaseModel):
    type: str = "auth_user_rejects"
    message: str = "User rejected connections"
