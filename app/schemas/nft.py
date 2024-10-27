from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class NFTPreviewSchema(BaseModel):
    resolution: str
    url: HttpUrl


class NFTCollectionMetadataSchema(BaseModel):
    cover_image: Optional[HttpUrl] = None
    description: str = ""
    marketplace: str = ""
    external_url: Optional[HttpUrl] = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: Optional[HttpUrl] = None


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
    image: Optional[HttpUrl] = None


class NFTItemSchema(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: Optional[NFTCollectionSchema] = None
    metadata: NFTItemMetadataSchema
    previews: List[NFTPreviewSchema]


class NFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema] = []
