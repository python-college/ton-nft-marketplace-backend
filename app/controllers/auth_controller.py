from fastapi import HTTPException
from app.utils.auth_utils import generate_auth_token
from app.models.auth_model import AuthModel
from app.schemas.auth import AuthResponceSchema, CheckAuthSchema


class AuthController:
    @staticmethod
    async def get_auth_token():
        token = generate_auth_token()
        auth = AuthModel(token)
        auth_link = await auth.connect_wallet()

        responce = AuthResponceSchema(auth_link=auth_link, token=token)
        return responce

    @staticmethod
    async def check_auth_token(token):
        auth = AuthModel(token)
        address = await auth.check_auth_token()
        if address:
            return CheckAuthSchema(address=address)
        raise HTTPException(status_code=403, detail="Unauthorized")
