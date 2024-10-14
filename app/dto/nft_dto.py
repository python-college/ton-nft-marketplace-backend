from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class NFTPreviewDTO(BaseModel):
    resolution: str
    url: HttpUrl


class NFTMetadataDTO(BaseModel):
    cover_image: HttpUrl = None
    description: str = ""
    marketplace: str = ""
    external_url: HttpUrl = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: HttpUrl = None


class NFTCollectionDTO(BaseModel):
    metadata: NFTMetadataDTO
    collection_address: str
    owner_address: str
    items_count: int
    previews: List[NFTPreviewDTO]
