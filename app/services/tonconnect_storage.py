from pytonconnect.storage import IStorage
import redis.asyncio as redis
from app.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USER,
    REDIS_USER_PASSWORD,
)

client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    username=REDIS_USER,
    password=REDIS_USER_PASSWORD,
)


class TonConnectStorage(IStorage):

    def __init__(self, session_id: str):
        self.session_id = session_id

    def _get_key(self, key: str):
        return f"{self.session_id}:{key}"

    async def set_item(self, key: str, value: str):
        await client.set(name=self._get_key(key), value=value)

    async def get_item(self, key: str, default_value: str = None):
        value = await client.get(name=self._get_key(key))
        return value.decode() if value else default_value

    async def remove_item(self, key: str):
        await client.delete(self._get_key(key))
