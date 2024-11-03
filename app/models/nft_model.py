from pytonapi import AsyncTonapi
from app.settings import IS_TESTNET, API_KEY


class NFTModel:
    def __init__(self):
        self.tonapi = AsyncTonapi(
            api_key=API_KEY,
            is_testnet=IS_TESTNET,
        )

    async def fetch_collection_data(self, collection_address: str):
        try:
            res = await self.tonapi.nft.get_collection_by_collection_address(
                account_id=collection_address
            )

            return {
                "metadata": res.metadata,
                "address": res.address.to_userfriendly(is_bounceable=True),
                "owner_address": res.owner.address.to_userfriendly(is_bounceable=True),
                "items_count": res.next_item_index,
                "previews": [
                    {"resolution": p.resolution, "url": p.url} for p in res.previews
                ],
            }
        except Exception as e:
            print(f"Error fetching collection: {e}")
            return None

    async def fetch_item_data(self, item_address: str):
        try:
            item = await self.tonapi.nft.get_item_by_address(account_id=item_address)

            return {
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
        except Exception as e:
            print(f"Error fetching collection: {e}")
            return None

    async def fetch_items_by_collection(self, collection_address: str):
        try:
            res = await self.tonapi.nft.get_items_by_collection_address(
                account_id=collection_address
            )

            return {
                "nft_items": [
                    {
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
                        "owner_address": item.owner.address.to_userfriendly(
                            is_bounceable=True
                        ),
                        "previews": [
                            {"resolution": p.resolution, "url": p.url}
                            for p in item.previews
                        ],
                    }
                    for item in res.nft_items
                ]
            }
        except Exception as e:
            print(f"Error fetching items: {e}")
            return None
