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
            previews = [
                NFTPreviewSchema(resolution=p["resolution"], url=p["url"])
                for p in collection_data["previews"]
            ]

            collection_schema = NFTCollectionSchema(
                metadata=collection_data["metadata"],
                collection_address=collection_data["address"],
                owner_address=collection_data["owner_address"],
                items_count=collection_data["next_item_index"],
                previews=previews,
            )
            return collection_schema
        else:
            raise HTTPException(status_code=404, detail="Collection not found")

    @staticmethod
    async def get_items_from_collection(collection_address: str):
        nft_model = NFTModel()
        items = await nft_model.fetch_items_by_collection(collection_address)

        if items:
            try:
                items_Schema = NFTItemsSchema(
                    nft_items=[
                        NFTItemSchema(
                            address=item["address"],
                            index=item["index"],
                            owner_address=item["owner_address"],
                            metadata=NFTItemMetadataSchema(
                                name=item["metadata"].get("name", ""),
                                description=item["metadata"].get("description", ""),
                                marketplace=item["metadata"].get("marketplace", ""),
                                image=item["metadata"].get("image"),
                            ),
                            previews=[
                                NFTPreviewSchema(
                                    resolution=p["resolution"], url=p["url"]
                                )
                                for p in item.get("previews", [])
                            ],
                        )
                        for item in items["nft_items"]
                    ],
                )
                return items_Schema
            except Exception as e:
                print(e)

        else:
            raise HTTPException(status_code=404, detail="Collection not found")

    @staticmethod
    async def get_item_by_address(nft_address: str):
        nft_model = NFTModel()
        item_data = await nft_model.fetch_item_data(nft_address)

        if item_data:
            previews = [
                NFTPreviewSchema(resolution=p["resolution"], url=p["url"])
                for p in item_data["previews"]
            ]

            collection_schema = NFTItemSchema(
                metadata=item_data["metadata"],
                address=item_data["address"],
                owner_address=item_data["owner_address"],
                index=item_data["index"],
                previews=previews,
            )
            return collection_schema
        else:
            raise HTTPException(status_code=404, detail="Item not found")
