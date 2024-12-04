import httpx
from typing import Dict, Any
from app.settings import CONTENT_SERVICE_HOST


class ContentServiceClient:
    def __init__(self):
        self.base_url = CONTENT_SERVICE_HOST
        self.timeout = 20

    async def fetch_item(self, nft_address: str) -> Dict[str, Any]:
        url = f"{self.base_url}/content/api/v1/nfts/{nft_address}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def fetch_collection(self, collection_address: str) -> Dict[str, Any]:
        url = f"{self.base_url}/content/api/v1/nfts/collections/{collection_address}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
