import json
from fastapi import WebSocket
from pydantic import ValidationError
from pytonconnect.exceptions import UserRejectsError
from app.schemas.management.mint import (
    MintCollectionSchema,
    MintCollectionUserRejectsSchema,
    MintCollectionDataProcessedSchema,
    MintCollectionSuccessSchema,
    MintCollectionSuccessPayload,
    MintNftSchema,
    MintNftUserRejectsSchema,
    MintNftDataProcessedSchema,
    MintNftSuccessSchema,
    MintNftSuccessPayload,
)
from app.schemas.management.sell import (
    SellNftSchema,
    SellNftUserRejectsSchema,
    SellNftSuccessSchema,
)
from app.schemas.management.buy import (
    BuyNftSchema,
    BuyNftUserRejectsSchema,
    BuyNftSuccessSchema,
)
from app.services.auth_service import AuthService
from app.services.management_service import ManagementService
from app.services.content_client import ContentServiceClient
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
        if not await AuthService.check_auth(session_id):
            await websocket.close(code=3003)
            return

        pinata_client = PinataClient()
        image_filename = pinata_client.upload_image(
            base64_image=collection_data.base64_image, file_name=collection_data.name
        )

        await websocket.send_json(MintCollectionDataProcessedSchema().model_dump())

        collection_data.image_name = image_filename

        try:
            collection_address = await ManagementService.mint_collection(collection_data)
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

    @staticmethod
    async def create_nft(websocket: WebSocket):
        await websocket.accept()
        content_service_client = ContentServiceClient()

        data = await websocket.receive_text()
        try:
            json_data = json.loads(data)
            nft_data = MintNftSchema(**json_data)
        except (json.JSONDecodeError, ValidationError):
            await websocket.close(code=1008)
            return

        session_id = nft_data.session_id
        if not await AuthService.check_auth(session_id):
            await websocket.close(code=3003)
            return

        pinata_client = PinataClient()
        image_filename = pinata_client.upload_image(
            base64_image=nft_data.base64_image, file_name=nft_data.name
        )

        await websocket.send_json(MintNftDataProcessedSchema().model_dump())

        nft_data.image_name = image_filename

        nft_data.index = int(
            (await content_service_client.fetch_collection(nft_data.collection_address))[
                "items_count"
            ]
        )

        try:
            await ManagementService.mint_nft(nft_data)
        except PermissionError:
            await websocket.close(code=3003)
        except UserRejectsError:
            await websocket.send_json(MintNftUserRejectsSchema().model_dump())
            await websocket.close(code=4008)
            return

        await websocket.send_json(
            MintNftSuccessSchema(
                payload=MintNftSuccessPayload(index=nft_data.index)
            ).model_dump()
        )
        await websocket.close()

    @staticmethod
    async def sell_nft(websocket: WebSocket):
        await websocket.accept()
        content_service_client = ContentServiceClient()

        data = await websocket.receive_text()
        try:
            json_data = json.loads(data)
            sell_data = SellNftSchema(**json_data)
        except (json.JSONDecodeError, ValidationError):
            await websocket.close(code=1008)
            return

        session_id = sell_data.session_id
        if not await AuthService.check_auth(session_id):
            await websocket.close(code=3003)
            return

        try:
            item_data = await content_service_client.fetch_item(sell_data.nft_address)
            collection_address = item_data["collection"]["address"]
            
            collection_data = await content_service_client.fetch_collection(collection_address)
            royalty_address = collection_data["owner_address"]

            sell_data.royalty_address = royalty_address
        except Exception:
            await websocket.close(code=4004)
            return

        try:
            await ManagementService.sell_nft(sell_data)
        except PermissionError:
            await websocket.close(code=3003)
        except UserRejectsError:
            await websocket.send_json(SellNftUserRejectsSchema().model_dump())
            await websocket.close(code=4008)
            return

        await websocket.send_json(SellNftSuccessSchema().model_dump())
        await websocket.close()

    @staticmethod
    async def buy_nft(websocket: WebSocket):
        await websocket.accept()
        content_service_client = ContentServiceClient()

        data = await websocket.receive_text()
        try:
            json_data = json.loads(data)
            buy_data = BuyNftSchema(**json_data)
        except (json.JSONDecodeError, ValidationError):
            await websocket.close(code=1008)
            return

        session_id = buy_data.session_id
        if not await AuthService.check_auth(session_id):
            await websocket.close(code=3003)
            return


        try:
            item_data = await content_service_client.fetch_item(buy_data.nft_address)

            if "sale" in item_data:
                price = int(item_data["sale"]["price"]["value"])
                contract_address = item_data["sale"]["contract_address"]
                buy_data.price = price
                buy_data.contract_address = contract_address
            else:
                await websocket.close(code=1008)
                return

        except Exception:
            await websocket.close(code=1008)
            return

        try:
            await ManagementService.buy_nft(buy_data)
        except PermissionError:
            await websocket.close(code=3003)
        except UserRejectsError:
            await websocket.send_json(BuyNftUserRejectsSchema().model_dump())
            await websocket.close(code=4008)
            return

        await websocket.send_json(BuyNftSuccessSchema().model_dump())
        await websocket.close()
