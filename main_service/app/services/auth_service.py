from pytoniq_core import Address
from app.utils.auth_utils import get_connector


class AuthService:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.connector = get_connector(session_id)

    async def connect_wallet(self) -> str:
        wallets_list = self.connector.get_wallets()
            
        wallet = wallets_list[1]
        generated_url = await self.connector.connect(wallet)

        generated_url = "tc://" + generated_url[len("https://app.tonkeeper.com/ton-connect"):]  

        if "r=" in generated_url:
            base, param = generated_url.split("r=", 1)
            param = param.replace("+", "%20")
            generated_url = base + "r=" + param

        return generated_url
    
    async def handle_auth(self):

        await self.connector.restore_connection()
        await self.connector.wait_for_connection()
        if self.connector.connected and self.connector.account.address:
            address = Address(self.connector.account.address).to_str(
                is_bounceable=True, is_user_friendly=True
            )
            return address
        return None

    @staticmethod
    async def check_auth(session_id: str):
        connector = get_connector(session_id)
        is_connected = await connector.restore_connection()
        if is_connected:
            return connector.account.address
        else:
            return None
