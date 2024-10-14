from fastapi import APIRouter
from app.controllers.nft_controller import NFTController
from app.dto.nft_dto import NFTCollectionDTO

router = APIRouter()


@router.get("/nfts/collections/{collection_address}", response_model=NFTCollectionDTO)
async def get_nft_collection(collection_address: str):
    return await NFTController.get_collection_by_address(collection_address)
