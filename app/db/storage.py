from pytonconnect.storage import IStorage
import redis.asyncio as redis
from app.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_USER, REDIS_USER_PASSWORD

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USER,
    password=REDIS_USER_PASSWORD
)


class Storage(IStorage):

    def __init__(self, token: str):
        self.token = token

    def _get_key(self, key: str):
        return str(self.token) + key

    async def set_item(self, key: str, value: str):
        await client.set(name=self._get_key(key), value=value)

    async def get_item(self, key: str, default_value: str = None):
        value = await client.get(name=self._get_key(key))
        return value.decode() if value else default_value

    async def remove_item(self, key: str):
        await client.delete(self._get_key(key))
