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
                "owner": res.owner.address.to_userfriendly(is_bounceable=False),
                "next_item_index": res.next_item_index,
                "previews": [
                    {"resolution": p.resolution, "url": p.url} for p in res.previews
                ],
            }
        except Exception as e:
            print(f"Error fetching collection: {e}")
            return None
