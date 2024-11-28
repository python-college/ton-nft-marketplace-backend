from fastapi import APIRouter, HTTPException, Query
from app.schemas import NFTItemSchema, NFTCollectionSchema, NFTItemsSchema, TopNFTItemsSchema, TopNFTCollectionSchema
from app.services.nft import NFTService
from app.services.collection import CollectionService
router = APIRouter()



@router.get("/nfts/{nft_address}", response_model=NFTItemSchema)
async def get_nft_item(nft_address: str):
    try:
        nft = await NFTService.get_item(nft_address)
        if nft is None:
            raise HTTPException(status_code=404, detail="Not found")
        return nft
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Invalid collection address format") from exc
    


@router.get(
    "/nfts/collections/{collection_address}", response_model=NFTCollectionSchema
)
async def get_nft_collection(collection_address: str):
    try:
        nft = await CollectionService.get_collection(collection_address)
        if nft is None:
            raise HTTPException(status_code=404, detail="Not found")
        return nft
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Invalid collection address format") from exc
    


@router.get(
    "/nfts/collections/{collection_address}/items", response_model=NFTItemsSchema
)
async def get_collection_items(collection_address: str):
    try:
        items = await NFTService.get_items(collection_address)
        if items is None:
            raise HTTPException(status_code=404, detail="Not found")
        return items
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Invalid collection address format") from exc


@router.get(
    "/top/nfts/", response_model=TopNFTItemsSchema
)
async def get_most_hype_items(
    page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Количество элементов на странице (от 1 до 100)")
):
    items = await NFTService.get_most_hype_items(page=page, page_size=page_size)
    return items

@router.get(
    "/top/collections/", response_model=TopNFTCollectionSchema
)
async def get_most_hype_collections(
    page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Количество элементов на странице (от 1 до 100)")
):
    collections = await CollectionService.get_most_hype_collections(page=page, page_size=page_size)
    return collections
