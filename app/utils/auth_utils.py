import secrets
import string
from pytonconnect import TonConnect
from app.settings import MANIFEST_URL, SESSION_ID_LENGTH
from app.services.tonconnect_storage import TonConnectStorage


def get_connector(session_id: str) -> TonConnect:
    return TonConnect(MANIFEST_URL, storage=TonConnectStorage(session_id))


def generate_session_id() -> str:
    characters = string.ascii_letters + string.digits
    session_id = "".join(secrets.choice(characters) for _ in range(SESSION_ID_LENGTH))
    return session_id
