from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.message_error_response import MessageErrorResponse
from ...models.products_page_response import ProductsPageResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 80,
    offset: int | Unset = 0,
    category_id: int | Unset = UNSET,
    search: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["category_id"] = category_id

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/order_bridge/products",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse | None:
    if response.status_code == 200:
        response_200 = ProductsPageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:

        def _parse_response_400(
            data: object,
        ) -> MessageErrorResponse | ValidationErrorResponse:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_400_type_0 = ValidationErrorResponse.from_dict(data)

                return response_400_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_400_type_1 = MessageErrorResponse.from_dict(data)

            return response_400_type_1

        response_400 = _parse_response_400(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 80,
    offset: int | Unset = 0,
    category_id: int | Unset = UNSET,
    search: str | Unset = UNSET,
) -> Response[MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse]:
    """Listado de productos (paginado)

    Args:
        limit (int | Unset):  Default: 80.
        offset (int | Unset):  Default: 0.
        category_id (int | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 80,
    offset: int | Unset = 0,
    category_id: int | Unset = UNSET,
    search: str | Unset = UNSET,
) -> MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse | None:
    """Listado de productos (paginado)

    Args:
        limit (int | Unset):  Default: 80.
        offset (int | Unset):  Default: 0.
        category_id (int | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 80,
    offset: int | Unset = 0,
    category_id: int | Unset = UNSET,
    search: str | Unset = UNSET,
) -> Response[MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse]:
    """Listado de productos (paginado)

    Args:
        limit (int | Unset):  Default: 80.
        offset (int | Unset):  Default: 0.
        category_id (int | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 80,
    offset: int | Unset = 0,
    category_id: int | Unset = UNSET,
    search: str | Unset = UNSET,
) -> MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse | None:
    """Listado de productos (paginado)

    Args:
        limit (int | Unset):  Default: 80.
        offset (int | Unset):  Default: 0.
        category_id (int | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | ProductsPageResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            category_id=category_id,
            search=search,
        )
    ).parsed
