from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sale_order_detail_response import SaleOrderDetailResponse
from ...models.simple_error_response import SimpleErrorResponse
from ...models.unauthorized_error_response import UnauthorizedErrorResponse
from ...types import Response


def _get_kwargs(
    order_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/order_bridge/orders/{order_id}".format(
            order_id=quote(str(order_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse | None:
    if response.status_code == 200:
        response_200 = SaleOrderDetailResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = UnauthorizedErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = SimpleErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    order_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse
]:
    """Detalle del pedido con líneas

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    order_id: int,
    *,
    client: AuthenticatedClient,
) -> SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse | None:
    """Detalle del pedido con líneas

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse
    """

    return sync_detailed(
        order_id=order_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    order_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse
]:
    """Detalle del pedido con líneas

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    order_id: int,
    *,
    client: AuthenticatedClient,
) -> SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse | None:
    """Detalle del pedido con líneas

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SaleOrderDetailResponse | SimpleErrorResponse | UnauthorizedErrorResponse
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
        )
    ).parsed
