from fastapi import HTTPException
from app.models.nft_model import NFTModel
from app.schemas.nft import (
    NFTCollectionSchema,
    NFTPreviewSchema,
    NFTItemsSchema,
    NFTItemSchema,
    NFTItemMetadataSchema,
)


class NFTController:
    @staticmethod
    async def get_collection_by_address(collection_address: str):
        nft_model = NFTModel()
        collection_data = await nft_model.fetch_collection_data(collection_address)

        if collection_data:
            collection_schema = NFTCollectionSchema(**collection_data)
            return collection_schema
        else:
            raise HTTPException(status_code=404, detail="Collection not found")

    @staticmethod
    async def get_items_from_collection(collection_address: str):
        nft_model = NFTModel()
        items = await nft_model.fetch_items_by_collection(collection_address)

        if items:
            items_schema = NFTItemsSchema(
                nft_items=[NFTItemSchema(**item) for item in items["nft_items"]],
            )
            return items_schema

        else:
            raise HTTPException(status_code=404, detail="Collection not found")

    @staticmethod
    async def get_item_by_address(nft_address: str):
        nft_model = NFTModel()
        item_data = await nft_model.fetch_item_data(nft_address)

        if item_data:
            collection_schema = NFTItemSchema(**item_data)
            return collection_schema
        else:
            raise HTTPException(status_code=404, detail="Item not found")
