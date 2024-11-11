from pydantic import BaseModel
from typing import Optional


class MintCollectionSchema(BaseModel):
    session_id: str
    name: str
    description: str
    royalty_base: int = 1000
    royalty_factor: int = 0
    base64_image: str
    image_name: Optional[str] = None


class MintCollectionUserRejectsSchema(BaseModel):
    type: str = "mint_collection_user_rejects"
    message: str = "User rejected transaction"


class MintCollectionDataProcessedSchema(BaseModel):
    type: str = "mint_collection_data_processed"
    message: str = "Data successfully received and processed"


class MintCollectionSuccessPayload(BaseModel):
    collection_address: str


class MintCollectionSuccessSchema(BaseModel):
    type: str = "mint_collection_success"
    payload: MintCollectionSuccessPayload


class MintNftSchema(BaseModel):
    session_id: str
    name: str
    description: str
    collection_address: str
    base64_image: str
    image_name: Optional[str] = None
    index: Optional[str] = None


class MintNftUserRejectsSchema(BaseModel):
    type: str = "mint_nft_user_rejects"
    message: str = "User rejected transaction"


class MintNftDataProcessedSchema(BaseModel):
    type: str = "mint_nft_data_processed"
    message: str = "Data successfully received and processed"


class MintNftSuccessPayload(BaseModel):
    index: int


class MintNftSuccessSchema(BaseModel):
    type: str = "mint_nft_success"
    payload: MintNftSuccessPayload


class SellNftSchema(BaseModel):
    session_id: str
    nft_address: str
    price: int
    royalty_address: Optional[str] = None


class SellNftUserRejectsSchema(BaseModel):
    type: str = "sell_nft_user_rejects"
    message: str = "User rejected transaction"


class SellNftSuccessSchema(BaseModel):
    type: str = "sell_nft_success"


class BuyNftSchema(BaseModel):
    session_id: str
    nft_address: str
    price: Optional[int] = None
    contract_address: Optional[str] = None


class BuyNftUserRejectsSchema(BaseModel):
    type: str = "buy_nft_user_rejects"
    message: str = "User rejected transaction"


class BuyNftSuccessSchema(BaseModel):
    type: str = "buy_nft_success"
