from tonsdk.utils import Address
from app.utils.auth_utils import get_connector


class AuthModel:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.connector = get_connector(session_id)

    async def connect_wallet(self) -> str:
        wallets_list = self.connector.get_wallets()
        wallet = wallets_list[1]
        generated_url = await self.connector.connect(wallet)
        return generated_url

    async def handle_auth(self):

        await self.connector.restore_connection()
        await self.connector.wait_for_connection()
        if self.connector.connected and self.connector.account.address:
            address = Address(self.connector.account.address).to_string(
                is_bounceable=True, is_user_friendly=True
            )
            return address
        return None

    @staticmethod
    async def check_auth(session_id: str):
        connector = get_connector(session_id)
        is_connected = await connector.restore_connection()
        return is_connected
