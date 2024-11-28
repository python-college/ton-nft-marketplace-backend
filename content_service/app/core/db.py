from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @staticmethod
    def connect_to_mongo():
        MongoDB.client = AsyncIOMotorClient(settings.MONGO_URL)
        MongoDB.db = MongoDB.client[settings.MONGO_DB_NAME]

    @staticmethod
    def close_mongo_connection():
        MongoDB.client.close()
