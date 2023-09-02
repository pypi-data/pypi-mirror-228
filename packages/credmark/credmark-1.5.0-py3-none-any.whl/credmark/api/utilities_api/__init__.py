from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, cast

from ...models.block_response import BlockResponse
from ...models.chains_response import ChainsResponse
from ...models.utilities_error_response import UtilitiesErrorResponse
from . import block_from_timestamp, block_to_timestamp, cross_chain_block, get_chains, get_latest_block


class UtilitiesApi:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def get_chains(
        self,
    ) -> ChainsResponse:
        """Get list of chains.

         Returns metadata for the list of blockchains supported by Credmark platform.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ChainsResponse]
        """

        return get_chains.sync(
            client=self.__client,
        )

    async def get_chains_async(
        self,
    ) -> ChainsResponse:
        """Get list of chains.

         Returns metadata for the list of blockchains supported by Credmark platform.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ChainsResponse]
        """

        return await get_chains.asyncio(
            client=self.__client,
        )

    def get_latest_block(
        self,
        chain_id: int,
    ) -> BlockResponse:
        """Get latest block.

         Returns latest block of the specified chain.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return get_latest_block.sync(
            client=self.__client,
            chain_id=chain_id,
        )

    async def get_latest_block_async(
        self,
        chain_id: int,
    ) -> BlockResponse:
        """Get latest block.

         Returns latest block of the specified chain.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return await get_latest_block.asyncio(
            client=self.__client,
            chain_id=chain_id,
        )

    def block_to_timestamp(
        self,
        chain_id: int,
        *,
        block_number: float,
    ) -> BlockResponse:
        """Convert block number to timestamp.

         Returns block timestamp of the specified block number.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            block_number (float): Block number.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return block_to_timestamp.sync(
            client=self.__client,
            chain_id=chain_id,
            block_number=block_number,
        )

    async def block_to_timestamp_async(
        self,
        chain_id: int,
        *,
        block_number: float,
    ) -> BlockResponse:
        """Convert block number to timestamp.

         Returns block timestamp of the specified block number.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            block_number (float): Block number.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return await block_to_timestamp.asyncio(
            client=self.__client,
            chain_id=chain_id,
            block_number=block_number,
        )

    def block_from_timestamp(
        self,
        chain_id: int,
        *,
        timestamp: float,
    ) -> BlockResponse:
        """Get block number from timestamp.

         Returns block on or before the specified block timestamp.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            timestamp (float): Unix timestamp - finds a block at or before the number of seconds since
                January 1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return block_from_timestamp.sync(
            client=self.__client,
            chain_id=chain_id,
            timestamp=timestamp,
        )

    async def block_from_timestamp_async(
        self,
        chain_id: int,
        *,
        timestamp: float,
    ) -> BlockResponse:
        """Get block number from timestamp.

         Returns block on or before the specified block timestamp.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            timestamp (float): Unix timestamp - finds a block at or before the number of seconds since
                January 1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return await block_from_timestamp.asyncio(
            client=self.__client,
            chain_id=chain_id,
            timestamp=timestamp,
        )

    def cross_chain_block(
        self,
        chain_id: int,
        *,
        block_number: float,
        cross_chain_id: int,
    ) -> BlockResponse:
        """Get equivalent cross-chain block.

         Returns cross chain's block on or before the timestamp of input chain's block number.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            block_number (float): Block number.
            cross_chain_id (int): Cross chain ID

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return cross_chain_block.sync(
            client=self.__client,
            chain_id=chain_id,
            block_number=block_number,
            cross_chain_id=cross_chain_id,
        )

    async def cross_chain_block_async(
        self,
        chain_id: int,
        *,
        block_number: float,
        cross_chain_id: int,
    ) -> BlockResponse:
        """Get equivalent cross-chain block.

         Returns cross chain's block on or before the timestamp of input chain's block number.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Ethereum Mainnet
                `10` - Optimism
                `56` - BSC
                `137` - Polygon Mainnet
                `250` - Fantom Opera
                `42161` - Arbitrum One
                `43114` - Avalanche C-Chain
            block_number (float): Block number.
            cross_chain_id (int): Cross chain ID

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[BlockResponse]
        """

        return await cross_chain_block.asyncio(
            client=self.__client,
            chain_id=chain_id,
            block_number=block_number,
            cross_chain_id=cross_chain_id,
        )
