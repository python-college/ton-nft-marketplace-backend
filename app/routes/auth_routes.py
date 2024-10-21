from fastapi import APIRouter
from app.controllers.auth_controller import AuthController
from app.schemas.auth import AuthResponceSchema, CheckAuthSchema

router = APIRouter()


@router.post("/auth/", response_model=AuthResponceSchema)
async def get_auth_token():
    return await AuthController.get_auth_token()


@router.post("/check-auth/{token}", response_model=CheckAuthSchema)
async def check_auth(token: str):
    return await AuthController.check_auth_token(token)
