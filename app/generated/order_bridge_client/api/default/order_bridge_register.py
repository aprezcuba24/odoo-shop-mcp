from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.register_body import RegisterBody
from ...models.register_ok_response import RegisterOkResponse
from ...models.simple_error_response import SimpleErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: RegisterBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/order_bridge/register",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse | None:
    if response.status_code == 200:
        response_200 = RegisterOkResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:

        def _parse_response_400(
            data: object,
        ) -> SimpleErrorResponse | ValidationErrorResponse:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_400_type_0 = ValidationErrorResponse.from_dict(data)

                return response_400_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_400_type_1 = SimpleErrorResponse.from_dict(data)

            return response_400_type_1

        response_400 = _parse_response_400(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterBody,
) -> Response[RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse]:
    """Registrar u obtener dispositivo

    Args:
        body (RegisterBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterBody,
) -> RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse | None:
    """Registrar u obtener dispositivo

    Args:
        body (RegisterBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterBody,
) -> Response[RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse]:
    """Registrar u obtener dispositivo

    Args:
        body (RegisterBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterBody,
) -> RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse | None:
    """Registrar u obtener dispositivo

    Args:
        body (RegisterBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RegisterOkResponse | SimpleErrorResponse | ValidationErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
