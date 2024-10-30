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
