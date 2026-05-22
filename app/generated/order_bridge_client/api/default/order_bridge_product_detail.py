from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.product_detail_response import ProductDetailResponse
from ...models.simple_error_response import SimpleErrorResponse
from ...types import Response


def _get_kwargs(
    product_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/order_bridge/products/{product_id}".format(
            product_id=quote(str(product_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProductDetailResponse | SimpleErrorResponse | None:
    if response.status_code == 200:
        response_200 = ProductDetailResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = SimpleErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProductDetailResponse | SimpleErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    product_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ProductDetailResponse | SimpleErrorResponse]:
    """Detalle de producto

    Args:
        product_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductDetailResponse | SimpleErrorResponse]
    """

    kwargs = _get_kwargs(
        product_id=product_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    product_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> ProductDetailResponse | SimpleErrorResponse | None:
    """Detalle de producto

    Args:
        product_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductDetailResponse | SimpleErrorResponse
    """

    return sync_detailed(
        product_id=product_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    product_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ProductDetailResponse | SimpleErrorResponse]:
    """Detalle de producto

    Args:
        product_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductDetailResponse | SimpleErrorResponse]
    """

    kwargs = _get_kwargs(
        product_id=product_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    product_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> ProductDetailResponse | SimpleErrorResponse | None:
    """Detalle de producto

    Args:
        product_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductDetailResponse | SimpleErrorResponse
    """

    return (
        await asyncio_detailed(
            product_id=product_id,
            client=client,
        )
    ).parsed
