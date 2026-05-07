from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.message_error_response import MessageErrorResponse
from ...models.order_cancel_response import OrderCancelResponse
from ...models.simple_error_response import SimpleErrorResponse
from ...models.unauthorized_error_response import UnauthorizedErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...types import Response


def _get_kwargs(
    order_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/order_bridge/orders/{order_id}/cancel".format(
            order_id=quote(str(order_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = OrderCancelResponse.from_dict(response.json())

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
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
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
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
]:
    """Cancelar pedido en borrador

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | OrderCancelResponse | SimpleErrorResponse | UnauthorizedErrorResponse]
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
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    """Cancelar pedido en borrador

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | OrderCancelResponse | SimpleErrorResponse | UnauthorizedErrorResponse
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
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
]:
    """Cancelar pedido en borrador

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageErrorResponse | ValidationErrorResponse | OrderCancelResponse | SimpleErrorResponse | UnauthorizedErrorResponse]
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
) -> (
    MessageErrorResponse
    | ValidationErrorResponse
    | OrderCancelResponse
    | SimpleErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    """Cancelar pedido en borrador

    Args:
        order_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageErrorResponse | ValidationErrorResponse | OrderCancelResponse | SimpleErrorResponse | UnauthorizedErrorResponse
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
        )
    ).parsed
