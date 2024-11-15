from fastapi import APIRouter, WebSocket
from app.controllers.auth_controller import AuthController

router = APIRouter()


@router.websocket("/ws/auth")
async def auth_websocket(websocket: WebSocket):
    await AuthController.auth_websocket(websocket)
