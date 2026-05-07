from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.message_error_response import MessageErrorResponse
from ...models.orders_page_response import OrdersPageResponse
from ...models.unauthorized_error_response import UnauthorizedErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    state: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["state"] = state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/order_bridge/orders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = OrdersPageResponse.from_dict(response.json())

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

    if response.status_code == 401:
        response_401 = UnauthorizedErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    state: str | Unset = UNSET,
) -> Response[
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
]:
    """Listar pedidos del contacto del dispositivo

    Args:
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | OrdersPageResponse | UnauthorizedErrorResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    state: str | Unset = UNSET,
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
    | None
):
    """Listar pedidos del contacto del dispositivo

    Args:
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | OrdersPageResponse | UnauthorizedErrorResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    state: str | Unset = UNSET,
) -> Response[
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
]:
    """Listar pedidos del contacto del dispositivo

    Args:
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | OrdersPageResponse | UnauthorizedErrorResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    state: str | Unset = UNSET,
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrdersPageResponse
    | UnauthorizedErrorResponse
    | None
):
    """Listar pedidos del contacto del dispositivo

    Args:
        limit (int | Unset):  Default: 50.
        offset (int | Unset):  Default: 0.
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | OrdersPageResponse | UnauthorizedErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            state=state,
        )
    ).parsed
