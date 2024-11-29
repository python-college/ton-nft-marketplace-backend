from pydantic import BaseModel
from typing import Optional


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