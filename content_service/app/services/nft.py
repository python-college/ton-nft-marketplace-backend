from tonsdk.utils import Address
from pytonapi.exceptions import TONAPINotFoundError
from app.repositories.nft import NFTRepository
from app.services.ton_api import TonApiService
from app.schemas import NFTItemSchema, NFTItemsSchema, TopNFTItemsSchema, SearchNFTItemsSchema


class NFTService:
    @staticmethod
    async def get_item(nft_address: str) -> NFTItemSchema | None:
        ton_service = TonApiService()
        try:
            raw_nft_address = Address(nft_address).to_string(
                is_bounceable=True, is_user_friendly=False
            )
        except Exception as exc:
            raise ValueError() from exc
        try:
            item_data = await ton_service.fetch_item_data(raw_nft_address)
        except TONAPINotFoundError:
            return None
        

        rarebay_item_data = await NFTRepository.get_nft_by_address(raw_nft_address)

        hype = rarebay_item_data.hype + 1 if rarebay_item_data is not None else 0
        item_data["hype"] = hype

        item_data_schema = NFTItemSchema(**item_data)
        await NFTRepository.update_nft(item_data_schema)
        return item_data_schema
    
    @staticmethod
    async def get_items(collection_address: str, limit: int = 20, offset: int = 0) -> NFTItemsSchema | None:
        ton_service = TonApiService()
        try:
            raw_collection_address = Address(collection_address).to_string(
                is_bounceable=True, is_user_friendly=False
            )
        except Exception as exc:
            raise ValueError() from exc

        try:
            items_data = await ton_service.fetch_items_by_collection(
                raw_collection_address,
                limit=limit,
                offset=offset,
            )
        except TONAPINotFoundError:
            return None

        for item in items_data:
            rarebay_item_data = await NFTRepository.get_nft_by_address(item["raw_address"])

            hype = rarebay_item_data.hype + 1 if rarebay_item_data is not None else 0
            item["hype"] = hype

        items_schema = NFTItemsSchema(
            nft_items=[NFTItemSchema(**item) for item in items_data],
        )
        for item in items_schema.nft_items:
            await NFTRepository.update_nft(item)

        return items_schema

    
    @staticmethod
    async def get_most_hype_items(page: int = 1, page_size: int = 20) -> TopNFTItemsSchema:
        return await NFTRepository.get_top_hyped_nfts(page=page, page_size=page_size)


    @staticmethod
    async def search_items(name: str, page: int = 1, page_size: int = 20) -> SearchNFTItemsSchema:
        return await NFTRepository.search_nfts(name=name, page=page, page_size=page_size)