import json
from fastapi import WebSocket
from pydantic import ValidationError
from pytonconnect.exceptions import UserRejectsError
from app.schemas.management import (
    MintCollectionSchema,
    MintCollectionUserRejectsSchema,
    MintCollectionDataProcessedSchema,
    MintCollectionSuccessSchema,
    MintCollectionSuccessPayload,
)
from app.models.auth_model import AuthModel
from app.models.management_collection_model import ManagementCollectionModel
from app.services.pinata_client import PinataClient


class ManagementController:

    @staticmethod
    async def create_collection(websocket: WebSocket):
        await websocket.accept()

        data = await websocket.receive_text()
        try:
            json_data = json.loads(data)
            collection_data = MintCollectionSchema(**json_data)
        except (json.JSONDecodeError, ValidationError):
            await websocket.close(code=1008)
            return

        session_id = collection_data.session_id
        if not await AuthModel.check_auth(session_id):
            await websocket.close(code=3003)
            return

        pinata_client = PinataClient()
        image_filename = pinata_client.upload_image(
            base64_image=collection_data.base64_image, file_name=collection_data.name
        )

        await websocket.send_json(MintCollectionDataProcessedSchema().model_dump())

        collection_data.image_name = image_filename

        try:
            collection_address = await ManagementCollectionModel.create_collection(
                collection_data
            )
        except PermissionError:
            await websocket.close(code=3003)
        except UserRejectsError:
            await websocket.send_json(MintCollectionUserRejectsSchema().model_dump())
            await websocket.close(code=4008)
            return

        await websocket.send_json(
            MintCollectionSuccessSchema(
                payload=MintCollectionSuccessPayload(
                    collection_address=collection_address
                )
            ).model_dump()
        )
        await websocket.close()
