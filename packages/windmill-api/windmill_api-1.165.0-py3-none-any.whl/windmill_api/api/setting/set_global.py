from typing import Any, Dict

import httpx

from ...client import Client
from ...models.set_global_json_body import SetGlobalJsonBody
from ...types import Response


def _get_kwargs(
    key: str,
    *,
    client: Client,
    json_body: SetGlobalJsonBody,
) -> Dict[str, Any]:
    url = "{}/settings/global/{key}".format(client.base_url, key=key)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    key: str,
    *,
    client: Client,
    json_body: SetGlobalJsonBody,
) -> Response[Any]:
    """post global settings

    Args:
        key (str):
        json_body (SetGlobalJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    key: str,
    *,
    client: Client,
    json_body: SetGlobalJsonBody,
) -> Response[Any]:
    """post global settings

    Args:
        key (str):
        json_body (SetGlobalJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        key=key,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
