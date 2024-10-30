import uuid
from pytonconnect import TonConnect
from app.settings import MANIFEST_URL
from app.services.tonconnect_storage import TonConnectStorage


def get_connector(session_id: str) -> TonConnect:
    return TonConnect(MANIFEST_URL, storage=TonConnectStorage(session_id))


def generate_session_id() -> str:
    return str(uuid.uuid4())
