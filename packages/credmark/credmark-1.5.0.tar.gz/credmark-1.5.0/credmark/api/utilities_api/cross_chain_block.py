from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict

from ... import errors
from ...models.block_response import BlockResponse
from ...models.utilities_error_response import UtilitiesErrorResponse
from ...types import UNSET, Response


def _get_kwargs(chain_id: int, *, block_number: float, cross_chain_id: int, client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/utilities/chains/{chainId}/block/cross-chain".format(client.base_url, chainId=chain_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["blockNumber"] = block_number

    params["crossChainId"] = cross_chain_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: "Credmark", response: httpx.Response) -> BlockResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = BlockResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UtilitiesErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[BlockResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: int, *, block_number: float, cross_chain_id: int, client: "Credmark"
) -> Response[BlockResponse]:
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

    kwargs = _get_kwargs(
        chain_id=chain_id,
        client=client,
        block_number=block_number,
        cross_chain_id=cross_chain_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(chain_id: int, *, block_number: float, cross_chain_id: int, client: "Credmark") -> BlockResponse:
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

    return sync_detailed(
        chain_id=chain_id,
        client=client,
        block_number=block_number,
        cross_chain_id=cross_chain_id,
    ).parsed


async def asyncio_detailed(
    chain_id: int, *, block_number: float, cross_chain_id: int, client: "Credmark"
) -> Response[BlockResponse]:
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

    kwargs = _get_kwargs(
        chain_id=chain_id,
        client=client,
        block_number=block_number,
        cross_chain_id=cross_chain_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(chain_id: int, *, block_number: float, cross_chain_id: int, client: "Credmark") -> BlockResponse:
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

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            client=client,
            block_number=block_number,
            cross_chain_id=cross_chain_id,
        )
    ).parsed
