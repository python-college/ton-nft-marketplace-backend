from pydantic import BaseModel
from typing import List


class NFTPreviewDTO(BaseModel):
    resolution: str
    url: str


class NFTCollectionDTO(BaseModel):
    # collection_name: str
    collection_address: str
    owner_address: str
    items_count: int
    previews: List[NFTPreviewDTO]
