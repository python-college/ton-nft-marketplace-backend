from base64 import urlsafe_b64encode
from datetime import datetime
from tonsdk.utils import Address
from tonutils.nft import (
    CollectionStandardModified,
    CollectionEditableModified,
)
from tonutils.nft.marketplace.getgems.contract.salev3r3 import SaleV3R3
from tonutils.nft.content import (
    CollectionModifiedOnchainContent,
    NFTModifiedOnchainContent,
)
from tonutils.nft.royalty_params import RoyaltyParams
from app.utils.auth_utils import get_connector
from app.schemas.management import MintCollectionSchema, MintNftSchema, SellNftSchema
from app.settings import (
    RAREBAY_ADDRESS,
    RAREBAY_FEE_ADDRESS,
    RAREBAY_FEE_RATE,
    RAREBAY_DEPLOYER_ADDRESS,
)


class ManagementModel:

    @staticmethod
    async def mint_collection(collection_data: MintCollectionSchema):
        connector = get_connector(collection_data.session_id)
        await connector.restore_connection()

        if not connector.connected:
            raise PermissionError()

        owner_address = connector.account.address

        collection = CollectionStandardModified(
            owner_address=Address(owner_address),
            next_item_index=0,
            content=CollectionModifiedOnchainContent(
                name=collection_data.name,
                description=collection_data.description,
                image=f"https://ipfs.io/ipfs/{collection_data.image_name}",
            ),
            royalty_params=RoyaltyParams(
                base=collection_data.royalty_base,
                factor=collection_data.royalty_factor,
                address=Address(owner_address),
            ),
        )

        transaction = {
            "valid_until": int(datetime.now().timestamp()) + 900,
            "messages": [
                {
                    "address": collection.address.to_str(),
                    "amount": "250000000",
                    "stateInit": urlsafe_b64encode(
                        collection.state_init.serialize().to_boc()
                    ).decode(),
                }
            ],
        }

        await connector.send_transaction(transaction)

        return collection.address.to_str()

    @staticmethod
    async def mint_nft(nft_data: MintNftSchema):
        connector = get_connector(nft_data.session_id)
        await connector.restore_connection()

        if not connector.connected:
            raise PermissionError()

        owner_address = connector.account.address

        body = CollectionEditableModified.build_mint_body(
            index=nft_data.index,
            owner_address=Address(owner_address),
            content=NFTModifiedOnchainContent(
                name=nft_data.name,
                description=nft_data.description,
                image=f"https://ipfs.io/ipfs/{nft_data.image_name}",
            ),
        )

        transaction = {
            "valid_until": int(datetime.now().timestamp()) + 900,
            "messages": [
                {
                    "address": nft_data.collection_address,
                    "amount": "250000000",
                    "payload": urlsafe_b64encode(body.to_boc()).decode(),
                }
            ],
        }

        await connector.send_transaction(transaction)

    @staticmethod
    async def sell_nft(sell_data: SellNftSchema):
        connector = get_connector(sell_data.session_id)
        await connector.restore_connection()

        if not connector.connected:
            raise PermissionError()

        marketplace_fee = int(sell_data.price * RAREBAY_FEE_RATE)
        royalty_fee = int(sell_data.price * 0.1)

        sale = SaleV3R3(
            nft_address=sell_data.nft_address,
            owner_address=connector.account.address,
            marketplace_address=RAREBAY_ADDRESS,
            marketplace_fee_address=RAREBAY_FEE_ADDRESS,
            royalty_address=sell_data.royalty_address,
            marketplace_fee=marketplace_fee,
            royalty_fee=royalty_fee,
            price=sell_data.price,
        )

        body = sale.build_transfer_nft_body(
            destination=RAREBAY_DEPLOYER_ADDRESS,
            owner_address=connector.account.address,
            state_init=sale.state_init,
        )

        transaction = {
            "valid_until": int(datetime.now().timestamp()) + 900,
            "messages": [
                {
                    "address": sell_data.nft_address,
                    "amount": "250000000",
                    "payload": urlsafe_b64encode(body.to_boc()).decode(),
                }
            ],
        }

        await connector.send_transaction(transaction)
