from fastapi import APIRouter, WebSocket
from app.controllers.management_controller import ManagementController

router = APIRouter()


@router.websocket("/ws/create/collection")
async def create_collection(websocket: WebSocket):
    await ManagementController.create_collection(websocket)


@router.websocket("/ws/create/nft")
async def create_nft(websocket: WebSocket):
    await ManagementController.create_nft(websocket)
