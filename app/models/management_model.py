from base64 import urlsafe_b64encode
from datetime import datetime
from tonsdk.utils import Address
from tonutils.nft import (
    CollectionStandardModified,
    CollectionEditableModified,
)
from tonutils.nft.content import (
    CollectionModifiedOnchainContent,
    NFTModifiedOnchainContent,
)
from tonutils.nft.royalty_params import RoyaltyParams
from app.utils.auth_utils import get_connector
from app.schemas.management import MintCollectionSchema, MintNftSchema


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
                    "amount": "50000000",
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
                    "amount": "50000000",
                    "payload": urlsafe_b64encode(body.to_boc()).decode(),
                }
            ],
        }

        await connector.send_transaction(transaction)
