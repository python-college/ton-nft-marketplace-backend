from fastapi import APIRouter, HTTPException, Query
from app.schemas import (
    NFTItemSchema,
    NFTCollectionSchema,
    NFTItemsSchema,
    TopNFTItemsSchema,
    TopNFTCollectionSchema,
    AccountSchema,
    SearchNFTCollectionSchema,
    SearchNFTItemsSchema
)
from app.services.nft import NFTService
from app.services.account import AccountService
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
async def get_collection_items(
    collection_address: str,
    limit: int = Query(20, ge=1, le=100, description="Number of items to return per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):

    try:
        items = await NFTService.get_items(collection_address, limit=limit, offset=offset)
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


@router.get("/accounts/{account_address}", response_model=AccountSchema)
async def get_account_data(account_address: str):
    try:
        account = await AccountService.get_account(account_address)
        if account is None:
            raise HTTPException(status_code=404, detail="Not found")
        return account
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Invalid collection address format") from exc
    


@router.get(
    "/accounts/{account_address}/items", response_model=NFTItemsSchema
)
async def get_account_items(account_address: str):
    try:
        items = await AccountService.get_items(account_address)
        if items is None:
            raise HTTPException(status_code=404, detail="Not found")
        return items
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Invalid collection address format") from exc
    

@router.get(
    "/search/nfts", response_model=SearchNFTItemsSchema
)
async def search_items(
    name: str,
    page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Количество элементов на странице (от 1 до 100)")
):
    items = await NFTService.search_items(name=name, page=page, page_size=page_size)
    return items


@router.get(
    "/search/collections", response_model=SearchNFTCollectionSchema
)
async def search_collections(
    name: str,
    page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Количество элементов на странице (от 1 до 100)")
):
    collections = await CollectionService.search_collections(name=name, page=page, page_size=page_size)
    return collections