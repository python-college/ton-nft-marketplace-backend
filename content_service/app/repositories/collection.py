from bson import ObjectId
from app.core.db import MongoDB
from app.schemas import NFTCollectionSchema, TopNFTCollectionSchema

class CollectionRepository:
    """
    Репозиторий для работы с коллекциями NFT в базе данных.

    Предоставляет методы для выполнения операций чтения, обновления и получения
    информации о самых хайповых коллекциях.
    """
    @staticmethod
    async def update_collection(collection: NFTCollectionSchema) -> bool:
        """
        Обновляет данные коллекции в базе данных.

        Если коллекция с заданным идентификатором существует, обновляет её данные.
        Если не существует, создаёт новую запись.

        :param collection: Объект схемы коллекции NFT.
        :return: True, если запись была обновлена, иначе False.
        """
        collection_data = collection.model_dump(mode="json")
        collection_data["_id"] = collection_data["raw_address"]
        result = await MongoDB.db["collections"].update_one(
            {"_id": collection_data["_id"]},
            {"$set": collection_data},
            upsert=True
        )
        return result.modified_count > 0

    @staticmethod
    async def get_collection_by_address(address: str) -> NFTCollectionSchema | None:
        """
        Ищет коллекцию NFT в базе данных по её адресу.

        Поддерживаются поиск по raw-адресу, userfriendly-адресу или идентификатору (_id).

        :param address: Адрес коллекции (raw или userfriendly).
        :return: Объект схемы коллекции NFT, если она найдена, иначе None.
        """
        query = {"$or": [
            {"_id": address},
            {"userfriendly_address": address},
            {"raw_address": address}
        ]}
        collection = await MongoDB.db["collections"].find_one(query)
        return NFTCollectionSchema(**collection) if collection else None

    @staticmethod
    async def get_most_hype_collections(page: int = 1, page_size: int = 20) -> TopNFTCollectionSchema:
        """
        Получает топ самых хайповых коллекций NFT с пагинацией.

        Коллекции сортируются по полю "hype" в порядке убывания.

        :param page: Номер страницы (по умолчанию 1).
        :param page_size: Количество элементов на странице (по умолчанию 20).
        :return: Объект TopNFTCollectionSchema
        """
        skip = (page - 1) * page_size
        cursor = MongoDB.db["collections"].find().sort("hype", -1).skip(skip).limit(page_size)
        collections = await cursor.to_list(length=page_size)
        total_count = await MongoDB.db["collections"].count_documents({})

        return TopNFTCollectionSchema(
            collections=[NFTCollectionSchema(**collection) for collection in collections],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
