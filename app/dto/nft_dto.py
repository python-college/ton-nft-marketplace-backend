from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class NFTPreviewDTO(BaseModel):
    resolution: str
    url: HttpUrl


class NFTCollectionMetadataDTO(BaseModel):
    cover_image: HttpUrl = None
    description: str = ""
    marketplace: str = ""
    external_url: HttpUrl = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: HttpUrl = None


class NFTCollectionDTO(BaseModel):
    metadata: NFTCollectionMetadataDTO
    collection_address: str
    owner_address: str
    items_count: int
    previews: List[NFTPreviewDTO]


class NFTItemMetadataDto(BaseModel):
    description: str = ""
    marketplace: str = ""
    name: str = ""
    image: HttpUrl = None


class NFTItemDTO(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: NFTCollectionDTO = None
    metadata: NFTItemMetadataDto
    previews: List[NFTPreviewDTO]


class NFTItemsDto(BaseModel):
    nft_items: List[NFTItemDTO] = []
