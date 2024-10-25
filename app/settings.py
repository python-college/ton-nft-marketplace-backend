import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
IS_TESTNET = os.getenv("IS_TESTNET") == "True"
MANIFEST_URL = os.getenv("MANIFEST_URL")

AUTH_TOKEN_LENGTH = 32

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_USER_PASSWORD = os.getenv("REDIS_USER_PASSWORD")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
