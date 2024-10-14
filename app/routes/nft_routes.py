from fastapi import APIRouter
from app.controllers.nft_controller import NFTController

router = APIRouter()


@router.get("/nfts/collections/{collection_address}")
async def get_nft_collection(collection_address: str):
    return await NFTController.get_collection_by_address(collection_address)
