from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict

from ... import errors
from ...models.chains_response import ChainsResponse
from ...models.utilities_error_response import UtilitiesErrorResponse
from ...types import Response


def _get_kwargs(client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/utilities/chains".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ChainsResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChainsResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UtilitiesErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ChainsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(client: "Credmark") -> Response[ChainsResponse]:
    """Get list of chains.

     Returns metadata for the list of blockchains supported by Credmark platform.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChainsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(client: "Credmark") -> ChainsResponse:
    """Get list of chains.

     Returns metadata for the list of blockchains supported by Credmark platform.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChainsResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(client: "Credmark") -> Response[ChainsResponse]:
    """Get list of chains.

     Returns metadata for the list of blockchains supported by Credmark platform.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChainsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(client: "Credmark") -> ChainsResponse:
    """Get list of chains.

     Returns metadata for the list of blockchains supported by Credmark platform.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChainsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
