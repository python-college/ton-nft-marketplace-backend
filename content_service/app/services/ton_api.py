from pytonapi import AsyncTonapi
from app.core.settings import settings


class TonApiService:
    def __init__(self):
        self.tonapi = AsyncTonapi(
            api_key=settings.TON_API_KEY,
            is_testnet=settings.IS_TESTNET,
        )

    async def fetch_collection_data(self, collection_address: str) -> dict:
        res = await self.tonapi.nft.get_collection_by_collection_address(
            account_id=collection_address
        )

        return {
            "metadata": res.metadata,
            "raw_address": res.address.to_raw(),
            "address": res.address.to_userfriendly(is_bounceable=True),
            "owner_address": res.owner.address.to_userfriendly(is_bounceable=True),
            "items_count": res.next_item_index,
            "previews": [
                {"resolution": p.resolution, "url": p.url} for p in res.previews
            ],
        }

    async def fetch_item_data(self, item_address: str) -> dict:
        item = await self.tonapi.nft.get_item_by_address(account_id=item_address)

        item_data = {
            "raw_address": item.address.to_raw(),
            "address": item.address.to_userfriendly(is_bounceable=True),
            "index": item.index,
            "metadata": item.metadata,
            "collection": {
                "address": item.collection.address.to_userfriendly(is_bounceable=True),
                "name": item.collection.name,
                "description": item.collection.description,
            },
            "owner_address": item.owner.address.to_userfriendly(is_bounceable=True),
            "previews": [
                {"resolution": p.resolution, "url": p.url} for p in item.previews
            ],
        }
        if item.sale is not None:
            item_data["sale"] = {
                "contract_address": item.sale.address.to_userfriendly(
                    is_bounceable=True
                ),
                "price": {
                    "value": item.sale.price.value,
                    "token_name": item.sale.price.token_name,
                },
            }
            if item.sale.owner is not None:
                item_data["sale"]["owner_address"] = (
                    item.sale.owner.address.to_userfriendly(is_bounceable=True)
                )

        return item_data

    async def fetch_items_by_collection(self, collection_address: str, limit: int = 20, offset: int = 0) -> list[dict]:
        res = await self.tonapi.nft.get_items_by_collection_address(
            account_id=collection_address,
            limit=limit,
            offset=offset,
        )

        nft_items = []
        for item in res.nft_items:
            item_data = {
                "raw_address": item.address.to_raw(),
                "address": item.address.to_userfriendly(is_bounceable=True),
                "index": item.index,
                "metadata": item.metadata,
                "collection": {
                    "address": item.collection.address.to_userfriendly(
                        is_bounceable=True
                    ),
                    "name": item.collection.name,
                    "description": item.collection.description,
                },
                "owner_address": item.owner.address.to_userfriendly(is_bounceable=True),
                "previews": [
                    {"resolution": p.resolution, "url": p.url} for p in item.previews
                ],
            }

            if item.sale is not None:
                sale_data = {
                    "contract_address": item.sale.address.to_userfriendly(
                        is_bounceable=True
                    ),
                    "price": {
                        "value": item.sale.price.value,
                        "token_name": item.sale.price.token_name,
                    },
                }
                if item.sale.owner is not None:
                    sale_data["owner_address"] = (
                        item.sale.owner.address.to_userfriendly(is_bounceable=True)
                    )

                item_data["sale"] = sale_data

            nft_items.append(item_data)

        return nft_items

    
    async def fetch_account_data(self, account_address: str) -> dict:
        res = await self.tonapi.accounts.get_info(
            account_id=account_address
        )

        return {
            "raw_address": res.address.to_raw(),
            "address": res.address.to_userfriendly(is_bounceable=True),
            "last_activity": res.last_activity,
            "balance": str(res.balance)
        }
    
    async def fetch_account_items(self, account_address: str) -> list[dict]:
        res = await self.tonapi.accounts.get_all_nfts(
            account_id=account_address
        )

        nft_items = []
        for item in res.nft_items:
            item_data = {
                "raw_address": item.address.to_raw(),
                "address": item.address.to_userfriendly(is_bounceable=True),
                "index": item.index,
                "metadata": item.metadata,
                "collection": {
                    "address": item.collection.address.to_userfriendly(
                        is_bounceable=True
                    ),
                    "name": item.collection.name,
                    "description": item.collection.description,
                },
                "owner_address": item.owner.address.to_userfriendly(is_bounceable=True),
                "previews": [
                    {"resolution": p.resolution, "url": p.url} for p in item.previews
                ],
            }

            if item.sale is not None:
                sale_data = {
                    "contract_address": item.sale.address.to_userfriendly(
                        is_bounceable=True
                    ),
                    "price": {
                        "value": item.sale.price.value,
                        "token_name": item.sale.price.token_name,
                    },
                }
                if item.sale.owner is not None:
                    sale_data["owner_address"] = (
                        item.sale.owner.address.to_userfriendly(is_bounceable=True)
                    )

                item_data["sale"] = sale_data

            nft_items.append(item_data)

        return nft_items