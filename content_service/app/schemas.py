from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Preview(BaseModel):
    resolution: str
    url: HttpUrl


class Price(BaseModel):
    value: str
    token_name: str


class Sale(BaseModel):
    contract_address: str
    owner_address: str
    price: Price


class Collection(BaseModel):
    address: str
    name: str
    description: str


class NFTCollectionMetadataSchema(BaseModel):
    cover_image: Optional[HttpUrl] = None
    description: str = ""
    marketplace: str = ""
    external_url: Optional[HttpUrl] = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: Optional[HttpUrl] = None


class NFTCollectionSchema(BaseModel):
    address: str
    raw_address: str
    metadata: NFTCollectionMetadataSchema
    hype: int
    owner_address: str
    items_count: int
    previews: List[Preview]


class NFTItemMetadata(BaseModel):
    description: str = ""
    marketplace: str = ""
    name: str = ""
    image: Optional[HttpUrl] = None


class NFTItemSchema(BaseModel):
    address: str
    raw_address: str
    index: int
    owner_address: Optional[str] = None
    collection: Optional[Collection] = None
    metadata: NFTItemMetadata
    hype: int
    sale: Optional[Sale] = None
    previews: List[Preview]


class NFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema] = []


class TopNFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema]
    total_count: int
    page: int
    page_size: int


class TopNFTCollectionSchema(BaseModel):
    collections: List[NFTCollectionSchema] = []
    total_count: int
    page: int
    page_size: int

class AccountSchema(BaseModel):
    address: str
    balance: int
    last_activity: int


class SearchNFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema]
    total_count: int
    page: int
    page_size: int


class SearchNFTCollectionSchema(BaseModel):
    collections: List[NFTCollectionSchema] = []
    total_count: int
    page: int
    page_size: int