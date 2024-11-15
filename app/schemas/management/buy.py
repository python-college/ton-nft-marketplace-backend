from pydantic import BaseModel
from typing import Optional


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