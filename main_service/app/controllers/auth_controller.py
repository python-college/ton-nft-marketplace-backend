from fastapi import WebSocket
from app.utils.auth_utils import generate_session_id
from app.models.auth_model import AuthModel
from app.schemas.auth import (
    AuthLinkSchema,
    AuthLinkPayload,
    AuthSuccessSchema,
    AuthSuccessPayload,
    AuthUserRejectsSchema,
)


class AuthController:

    @staticmethod
    async def auth_websocket(websocket: WebSocket):
        await websocket.accept()

        session_id = generate_session_id()
        auth = AuthModel(session_id)

        auth_link = await auth.connect_wallet()
        await websocket.send_json(
            AuthLinkSchema(payload=AuthLinkPayload(auth_link=auth_link)).model_dump()
        )

        address = await auth.handle_auth()
        if address:
            await websocket.send_json(
                AuthSuccessSchema(
                    payload=AuthSuccessPayload(address=address, session_id=session_id)
                ).model_dump()
            )
        else:
            await websocket.send_json(AuthUserRejectsSchema().model_dump())
            await websocket.close(code=4008)

        await websocket.close()
