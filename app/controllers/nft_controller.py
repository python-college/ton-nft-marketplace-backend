from app.models.nft_model import NFTModel
from app.dto.nft_dto import NFTCollectionDTO, NFTPreviewDTO


class NFTController:
    @staticmethod
    async def get_collection_by_address(collection_address: str):
        nft_model = NFTModel()
        collection_data = await nft_model.fetch_collection_data(collection_address)

        if collection_data:
            previews = [
                NFTPreviewDTO(resolution=p["resolution"], url=p["url"])
                for p in collection_data["previews"]
            ]

            collection_dto = NFTCollectionDTO(
                # collection_name=collection_data["metadata"],
                collection_address=collection_data["address"],
                owner_address=collection_data["owner"],
                items_count=collection_data["next_item_index"],
                previews=previews,
            )
            return collection_dto
        else:
            return {"error": "Collection not found"}
