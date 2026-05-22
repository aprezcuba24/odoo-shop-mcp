from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configuration_error_response import ConfigurationErrorResponse
from ...models.push_token_body import PushTokenBody
from ...models.push_topics_ok_response import PushTopicsOkResponse
from ...models.simple_error_response import SimpleErrorResponse
from ...models.unauthorized_error_response import UnauthorizedErrorResponse
from ...models.validation_error_response import ValidationErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: PushTokenBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/order_bridge/push/token",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = PushTopicsOkResponse.from_dict(response.json())

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

    if response.status_code == 401:
        response_401 = UnauthorizedErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 503:
        response_503 = ConfigurationErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
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
    body: PushTokenBody,
) -> Response[
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
    | UnauthorizedErrorResponse
]:
    """Registrar o actualizar token FCM y suscribir topics

    Args:
        body (PushTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationErrorResponse | PushTopicsOkResponse | SimpleErrorResponse | ValidationErrorResponse | UnauthorizedErrorResponse]
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
    client: AuthenticatedClient,
    body: PushTokenBody,
) -> (
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    """Registrar o actualizar token FCM y suscribir topics

    Args:
        body (PushTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationErrorResponse | PushTopicsOkResponse | SimpleErrorResponse | ValidationErrorResponse | UnauthorizedErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PushTokenBody,
) -> Response[
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
    | UnauthorizedErrorResponse
]:
    """Registrar o actualizar token FCM y suscribir topics

    Args:
        body (PushTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationErrorResponse | PushTopicsOkResponse | SimpleErrorResponse | ValidationErrorResponse | UnauthorizedErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PushTokenBody,
) -> (
    ConfigurationErrorResponse
    | PushTopicsOkResponse
    | SimpleErrorResponse
    | ValidationErrorResponse
    | UnauthorizedErrorResponse
    | None
):
    """Registrar o actualizar token FCM y suscribir topics

    Args:
        body (PushTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationErrorResponse | PushTopicsOkResponse | SimpleErrorResponse | ValidationErrorResponse | UnauthorizedErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
