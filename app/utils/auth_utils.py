import secrets
import string
from pytonconnect import TonConnect
from app.settings import AUTH_TOKEN_LENGTH, MANIFEST_URL
from app.db.storage import Storage


def generate_auth_token():
    characters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(characters) for _ in range(AUTH_TOKEN_LENGTH))
    return token


def get_connector(token: string):
    return TonConnect(MANIFEST_URL, storage=Storage(token))
