from tonsdk.utils import Address
from pytonapi.exceptions import TONAPINotFoundError
from app.services.ton_api import TonApiService
from app.repositories.collection import CollectionRepository
from app.schemas import NFTCollectionSchema, TopNFTCollectionSchema, SearchNFTCollectionSchema

class CollectionService:
    @staticmethod
    async def get_collection(collection_address: str) -> NFTCollectionSchema | None:
        ton_service = TonApiService()
        try:
            raw_collection_address = Address(collection_address).to_string(
                is_bounceable=True, is_user_friendly=False
            )
        except Exception as exc:
            raise ValueError() from exc

        try:
            collection_data = await ton_service.fetch_collection_data(raw_collection_address)
        except TONAPINotFoundError:
            return None

        rarebay_collection_address = await CollectionRepository.get_collection_by_address(raw_collection_address)

        hype = rarebay_collection_address.hype + 1 if rarebay_collection_address is not None else 0
        collection_data["hype"] = hype

        item_data_schema = NFTCollectionSchema(**collection_data)
        await CollectionRepository.update_collection(item_data_schema)
        return item_data_schema
    
    @staticmethod
    async def get_most_hype_collections(page: int = 1, page_size: int = 20) -> TopNFTCollectionSchema:
        return await CollectionRepository.get_most_hype_collections(page=page, page_size=page_size)
    
    @staticmethod
    async def search_collections(name: str, page: int = 1, page_size: int = 20) -> SearchNFTCollectionSchema:
        return await CollectionRepository.search_collections(name=name, page=page, page_size=page_size)
