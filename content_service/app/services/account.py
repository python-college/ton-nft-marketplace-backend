from tonsdk.utils import Address
from pytonapi.exceptions import TONAPINotFoundError
from app.services.ton_api import TonApiService
from app.schemas import AccountSchema, NFTItemsSchema, NFTItemSchema, SearchNFTItemsSchema
from app.repositories.nft import NFTRepository



class AccountService:
    @staticmethod
    async def get_account(account_address: str) -> AccountSchema | None:
        ton_service = TonApiService()
        try:
            raw_account_address = Address(account_address).to_string(
                is_bounceable=True, is_user_friendly=False
            )
        except Exception as exc:
            raise ValueError() from exc
        try:
            account_data = await ton_service.fetch_account_data(raw_account_address)
        except TONAPINotFoundError:
            return None
        

        item_data_schema = AccountSchema(**account_data)
        return item_data_schema


    @staticmethod
    async def get_items(account_address: str) -> NFTItemsSchema | None:
        ton_service = TonApiService()
        try:
            raw_account_address = Address(account_address).to_string(
                is_bounceable=True, is_user_friendly=False
            )
        except Exception as exc:
            raise ValueError() from exc

        try:
            items_data = await ton_service.fetch_account_items(raw_account_address)
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
    async def search_items(name: str, page: int = 1, page_size: int = 20) :
        return await NFTRepository.search_nfts(name=name, page=page, page_size=page_size)

