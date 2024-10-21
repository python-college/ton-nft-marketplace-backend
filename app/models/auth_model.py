from tonsdk.utils import Address
from app.utils.auth_utils import get_connector


class AuthModel:
    def __init__(self, token):
        self.token = token

    async def connect_wallet(self):
        connector = get_connector(self.token)
        wallets_list = connector.get_wallets()
        wallet = wallets_list[0]
        generated_url = await connector.connect(wallet)
        return generated_url

    async def check_auth_token(self):
        connector = get_connector(self.token)
        await connector.restore_connection()

        if connector.connected and connector.account.address:
            address = Address(connector.account.address).to_string(
                is_bounceable=True, is_user_friendly=True
            )
            return address
        return None
