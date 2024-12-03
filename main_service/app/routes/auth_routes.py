from fastapi import APIRouter, WebSocket, Header
from app.controllers.auth_controller import AuthController
from app.schemas.auth import AuthSuccessSchema

router = APIRouter()


@router.websocket("/ws/auth")
async def auth_websocket(websocket: WebSocket):
    await AuthController.auth_websocket(websocket)


@router.get("/check-auth")
async def chech_auth(session_id: str = Header(...)):
    return await AuthController.check_auth(session_id)