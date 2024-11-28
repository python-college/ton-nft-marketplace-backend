from bson import ObjectId
from app.core.db import MongoDB
from app.schemas import NFTItemSchema, TopNFTItemsSchema

class NFTRepository:
    """
    Репозиторий для работы с NFT-элементами в базе данных.

    Предоставляет методы для выполнения операций обновления данных итемов
    и получения самых хайповых NFT.
    """
    
    @staticmethod
    async def update_nft(nft: NFTItemSchema) -> bool:
        """
        Обновляет данные NFT в базе данных.

        Если NFT с заданным идентификатором существует, обновляет её данные.
        Если не существует, создаёт новую запись (upsert).

        :param nft: Объект схемы NFT.
        :return: True, если запись была обновлена, иначе False.
        """
        nft_data = nft.model_dump(mode="json")
        nft_data["_id"] = nft_data["raw_address"]
        
        result = await MongoDB.db["nfts"].update_one(
            {"_id": nft_data["_id"]},
            {"$set": nft_data},
            upsert=True
        )
        return result.modified_count > 0

    @staticmethod
    async def get_nft_by_address(address: str) -> NFTItemSchema | None:
        """
        Ищет NFT в базе данных по его адресу.

        Поддерживаются поиск по raw-адресу и userfriendly-адресу

        :param address: Адрес NFT (raw или userfriendly).
        :return: Объект схемы NFT, если он найден, иначе None.
        """
        query = {"$or": [
            {"_id": address},
            {"userfriendly_address": address},
            {"raw_address": address}
        ]}
        nft = await MongoDB.db["nfts"].find_one(query)
        return NFTItemSchema(**nft) if nft else None

    @staticmethod
    async def get_top_hyped_nfts(page: int = 1, page_size: int = 20) -> TopNFTItemsSchema:
        """
        Получает топ самых хайповых NFT с пагинацией.

        NFT сортируются по полю "hype" в порядке убывания.

        :param page: Номер страницы (по умолчанию 1).
        :param page_size: Количество элементов на странице (по умолчанию 20).
        :return: Объект TopNFTItemsSchema, содержащий NFT, общее количество и данные пагинации.
        """
        skip = (page - 1) * page_size
        cursor = MongoDB.db["nfts"].find().sort("hype", -1).skip(skip).limit(page_size)
        nfts = await cursor.to_list(length=page_size)
        total_count = await MongoDB.db["nfts"].count_documents({})

        return TopNFTItemsSchema(
            nft_items=[NFTItemSchema(**nft) for nft in nfts],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
