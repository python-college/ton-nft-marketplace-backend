from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class NFTPreviewSchema(BaseModel):
    resolution: str
    url: HttpUrl


class NFTCollectionMetadataSchema(BaseModel):
    cover_image: HttpUrl = None
    description: str = ""
    marketplace: str = ""
    external_url: HttpUrl = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: HttpUrl = None


class NFTCollectionSchema(BaseModel):
    metadata: NFTCollectionMetadataSchema
    collection_address: str
    owner_address: str
    items_count: int
    previews: List[NFTPreviewSchema]


class NFTItemMetadataSchema(BaseModel):
    description: str = ""
    marketplace: str = ""
    name: str = ""
    image: HttpUrl = None


class NFTItemSchema(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: NFTCollectionSchema = None
    metadata: NFTItemMetadataSchema
    previews: List[NFTPreviewSchema]


class NFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema] = []
